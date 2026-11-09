"""Generate notebooks/llm_harness.ipynb."""
import json
import os

cells = []


def md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "id": f"md-{len(cells)}",
                  "source": text.splitlines(True)})


def code(text):
    cells.append({"cell_type": "code", "metadata": {}, "id": f"code-{len(cells)}",
                  "execution_count": None, "outputs": [], "source": text.splitlines(True)})


md("""# LLM Harness — step by step

Shows exactly how we call the LLM, using the same functions as the prototype
(`src/llm_compiler.py` + `src/mcp_server.py`):

1. Build the payload (per-slice telemetry + ML signals).
2. **No-tool** call: plain JSON (`call_llm_model`).
3. **Tool harness**: multi-round tool-calling (`call_llm_with_tools`), reconstructed
   step by step so you see the raw `tool_calls` and tool results.
""")

code("""%matplotlib inline
import sys, os, json
for _p in (os.getcwd(), os.path.dirname(os.getcwd())):
    if os.path.exists(os.path.join(_p, "src")):
        sys.path.insert(0, _p)
        os.chdir(_p)
        break

import numpy as np
from src import benchmark as bench
from src import capacity_model as cm
from src.dataset import load_result_dir, sorted_by_load
from src.kpi_predictor import MLPRegressor, violation_prob
from src.forecaster import LinearForecaster
from src.llm_compiler import build_payload, call_llm_model, SYSTEM_TOOL, _post
from src.mcp_server import call_tool, openai_tools

DATA = "datasets/generation_netwok_slicing_dataset/2.2.1-10kprocessed/results_slicing_WFQ_1000_routing_7800_7899"
MODEL = "glm-5.3-flash:cloud"
""")

code("""states, delays, losses = load_result_dir(DATA)
states, delays, losses = sorted_by_load(states, delays, losses)
cfgs = bench.build_cfgs(states, delays)
agg_nf = bench.build_agg_nf(states, delays)
agg = [sum(s.values()) for s in states]
predictor = MLPRegressor().fit(agg, delays)
fc = LinearForecaster(window=5)

i = 40
state = states[i]
obs = {"t": i, "slices": {s: {"load": state[s], "replicas": 1,
    "delay": cm.delay(state[s], 1, cfgs[s]), "loss": cm.loss(state[s], 1, cfgs[s])} for s in cm.SLICES}}
history = list(agg[:i+1])
forecast = fc.predict(history)
pv = violation_prob(float(predictor.predict([forecast])[0]), agg_nf.delay_budget)
payload = build_payload(obs, forecast, pv, cfgs)

print("per-slice load:", {s: round(state[s]) for s in cm.SLICES})
print("forecast:", round(forecast), "Mbps  p_violation:", round(pv, 3))
print("payload:")
print(json.dumps(payload, indent=2)[:600], "...")
""")

md("""## 1. The system prompt

The same `SYSTEM_TOOL` string the harness sends as the system message.""")
code("""print(SYSTEM_TOOL)""")

md("""## 2. The tools

`openai_tools` converts our MCP tool schemas into OpenAI function-calling
format. Here we expose `inspect_infrastructure` and `scale_replicas`.""")
code("""tools = openai_tools(["inspect_infrastructure", "scale_replicas"])
print(json.dumps(tools, indent=2))""")

md("""## 3. No-tool call

`call_llm_model` — one HTTP round, the model answers JSON directly (no tools).""")
code("""r = call_llm_model(MODEL, payload, cfgs)
print("raw response:", r["raw"])
print("actions:", r["actions"])
print("latency_ms:", round(r["latency_ms"], 1))""")

md("""## 4. Tool harness, step by step

`call_llm_with_tools` does a multi-round loop. We reconstruct it here so you
see each round: the assistant asks for tool calls, we execute them against the
MCP server, feed the results back. The answer is the model's `scale_replicas`
calls — no JSON.""")
code("""messages = [
    {"role": "system", "content": SYSTEM_TOOL},
    {"role": "user", "content": json.dumps(payload)},
]
print("tool names sent:", [t["function"]["name"] for t in tools])

trace = []
for round_ in range(4):
    data = _post(messages, tools=tools, model=MODEL)
    msg = data["choices"][0]["message"]
    print(f"\\n=== round {round_+1} — finish_reason: "
          f"{data['choices'][0].get('finish_reason')} ===")
    if not msg.get("tool_calls"):
        print("no more tool calls — model done")
        break
    print("assistant tool_calls:")
    print(json.dumps(msg["tool_calls"], indent=2))
    messages.append({"role": "assistant", "content": msg.get("content") or "",
                     "tool_calls": msg["tool_calls"]})
    for tc in msg["tool_calls"]:
        fn = tc["function"]
        name = fn["name"]
        args = json.loads(fn.get("arguments") or "{}")
        result = call_tool(name, args, cfgs)
        trace.append({"name": name, "args": args, "result": result})
        print(f"--- execute {name}({args}) ->")
        print(json.dumps(result, indent=2))
        messages.append({"role": "tool", "tool_call_id": tc.get("id", f"c{round_}"),
                         "content": json.dumps(result)})

# the answer = the last successful scale_replicas call per slice
actions = {s: payload["slices"][s]["replicas"] for s in cm.SLICES}
for tc in trace:
    if tc["name"] == "scale_replicas":
        st = tc["args"].get("slice_type")
        if st in cm.SLICES and tc["result"].get("ok"):
            actions[st] = tc["result"]["replicas"]
print("actions (from scale_replicas calls):", actions)
""")

nb = {
    "nbformat": 4, "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.14"},
    },
    "cells": cells,
}

os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notebooks"), exist_ok=True)
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notebooks", "llm_harness.ipynb")
with open(out, "w") as f:
    json.dump(nb, f, indent=1)
print("wrote", out)

"""Payload builder + LLM decision (Tier 2), per slice.

`build_payload` compacts per-slice telemetry + ML signals. `call_stub` is a
deterministic offline stub. `call_llm_model` makes one real call to an
OpenAI-compatible endpoint (Ollama cloud models over localhost, no token).
"""
import json
import os
import time
import urllib.request
import urllib.error

from .capacity_model import SLICES, required_replicas
from .mcp_server import call_tool, openai_tools


def build_payload(obs, forecast, p_violation, cfgs):
    return {
        "slices": {s: {
            "kpi_target": {"delay": cfgs[s].delay_budget, "loss": cfgs[s].loss_budget},
            "kpi_now": {"delay": obs["slices"][s]["delay"], "loss": obs["slices"][s]["loss"]},
            "load_mbps": obs["slices"][s]["load"],
            "replicas": obs["slices"][s]["replicas"],
            "max_replicas": cfgs[s].max_replicas,
        } for s in SLICES},
        "ml": {"aggregate_forecast_mbps": forecast, "p_violation": p_violation},
    }


def call_stub(payload, cfgs):
    """Stub: mimic a competent LLM reading the payload. No network."""
    pv = payload["ml"]["p_violation"]
    actions = {}
    for s in SLICES:
        sl = payload["slices"][s]
        req = required_replicas(sl["load_mbps"], cfgs[s])
        cur = sl["replicas"]
        if pv > 0.5 and req > cur:
            actions[s] = req
        elif pv < 0.1 and cur > cfgs[s].min_replicas:
            actions[s] = max(cfgs[s].min_replicas, cur - 1)
        else:
            actions[s] = cur
    return {"actions": actions, "reason": "stub"}


def ollama_config():
    base = os.environ.get("OLLAMA_BASE_URL") or "http://localhost:11434/v1"
    key = os.environ.get("OLLAMA_API_KEY") or ""
    model = os.environ.get("SLICING_LLM_MODEL") or "deepseek-v4-pro:cloud"
    return base, key, model


def chat(base, key, model, system, user, retries=6):
    body = json.dumps({"model": model, "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ], "temperature": 0.0}).encode()
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    url = base.rstrip("/") + "/chat/completions"
    t0 = time.time()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=body, headers=headers)
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read().decode())
            latency_ms = (time.time() - t0) * 1000.0
            content = data["choices"][0]["message"]["content"]
            return content, data.get("usage", {}), latency_ms
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if attempt < retries - 1:
                time.sleep(15 * (attempt + 1))
                continue
            raise


def call_llm_model(model, payload, cfgs, base=None, key=None):
    base = base or "http://localhost:11434/v1"
    system = (
        "You are the Tier-2 compiler of a 6G network-slicing control plane. "
        "You receive per-slice telemetry (eMBB, URLLC, mMTC): load (Mbps), "
        "current replicas, current delay/loss, KPI targets, and ML signals "
        "(aggregate load forecast, violation probability). Decide the replica "
        "count for each slice. Output ONLY a JSON object: "
        '{"actions": {"eMBB": <int>, "URLLC": <int>, "mMTC": <int>}, "reason": "<short>"}. '
        "Replica counts are integers in [1,5]. No prose outside the JSON."
    )
    content, usage, latency_ms = chat(base, key or "", model, system, json.dumps(payload))
    start, end = content.find("{"), content.rfind("}")
    obj = {}
    if start >= 0 and end >= 0:
        try:
            obj = json.loads(content[start:end + 1])
        except json.JSONDecodeError:
            obj = {}
    actions = {}
    for s in SLICES:
        try:
            actions[s] = int(obj.get("actions", {}).get(s, payload["slices"][s]["replicas"]))
        except (TypeError, ValueError):
            actions[s] = payload["slices"][s]["replicas"]
    return {"model": model, "actions": actions,
            "reason": obj.get("reason", ""), "raw": content,
            "usage": usage, "latency_ms": latency_ms}


SYSTEM_TOOL = (
    "You are the Tier-2 compiler of a 6G network-slicing control plane. "
    "You receive per-slice telemetry (eMBB, URLLC, mMTC): load (Mbps), current "
    "replicas, current delay/loss, KPI targets, and ML signals. Use the provided "
    "tools to compute the correct replica count. Then act: call scale_replicas "
    "once per slice (eMBB, URLLC, mMTC) with the replica count you decide. "
    "Do not output text or JSON - your scale_replicas calls are the answer."
)


def _post(messages, tools=None, base=None, key=None, model=None):
    body = {"model": model, "messages": messages, "temperature": 0.0}
    if tools:
        body["tools"] = tools
        body["tool_choice"] = "auto"
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    url = (base or "http://localhost:11434/v1").rstrip("/") + "/chat/completions"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def call_llm_with_tools(model, payload, cfgs, tool_names,
                        base=None, key=None, max_rounds=6):
    """Tool-calling harness: LLM may call MCP tools, then returns the action."""
    base = base or "http://localhost:11434/v1"
    messages = [
        {"role": "system", "content": SYSTEM_TOOL},
        {"role": "user", "content": json.dumps(payload)},
    ]
    tools = openai_tools(tool_names)
    used = []
    trace = []
    usage = {}
    t0 = time.time()
    for _ in range(max_rounds):
        data = _post(messages, tools=tools, base=base, key=key or "", model=model)
        usage = data.get("usage", {})
        msg = data["choices"][0]["message"]
        if not msg.get("tool_calls"):
            break  # model done; the decision is in the tool-call history
        messages.append({"role": "assistant", "content": msg.get("content") or "",
                         "tool_calls": msg["tool_calls"]})
        for tc in msg["tool_calls"]:
            fn = tc["function"]
            name = fn["name"]
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            try:
                result = call_tool(name, args, cfgs)
            except Exception as e:
                result = {"error": str(e)}
            used.append(name)
            trace.append({"name": name, "args": args, "result": result})
            messages.append({"role": "tool",
                             "tool_call_id": tc.get("id", f"call_{len(used)}"),
                             "content": json.dumps(result)})
    # derive the action from the last successful scale_replicas call per slice
    actions = {s: payload["slices"][s]["replicas"] for s in SLICES}
    for tc in trace:
        if tc["name"] == "scale_replicas":
            st = tc["args"].get("slice_type")
            if st in SLICES and tc["result"].get("ok"):
                actions[st] = tc["result"]["replicas"]
    return {"model": model, "actions": actions, "reason": "tool-calls",
            "raw": "", "tools_used": used, "trace": trace, "usage": usage,
            "latency_ms": (time.time() - t0) * 1000.0}

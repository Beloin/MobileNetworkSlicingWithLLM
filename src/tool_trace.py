"""Capture full function-call traces for the inspect tool (resumable).

Records every tool call (name, args, result) per decision so we can verify
what the models actually call. Saves to results/tool_trace.json.
"""
import json
import os
import time

from . import benchmark as bench
from . import capacity_model as cm
from .dataset import load_result_dir, sorted_by_load
from .kpi_predictor import MLPRegressor, violation_prob
from .forecaster import LinearForecaster
from .llm_compiler import build_payload, call_llm_with_tools

MODELS = ["glm-5.3-flash:cloud", "deepseek-v4-pro:cloud", "glm-5.3:cloud"]
OUT = os.path.join(bench.REPO_ROOT, "results", "tool_trace.json")


def main():
    results = json.load(open(OUT)) if os.path.exists(OUT) else {}

    states, delays, losses = load_result_dir(bench.DEFAULT_DIR)
    states, delays, losses = sorted_by_load(states, delays, losses)
    cfgs = bench.build_cfgs(states, delays)
    agg_nf = bench.build_agg_nf(states, delays)
    agg = [sum(s.values()) for s in states]
    predictor = MLPRegressor().fit(agg, delays)
    fc = LinearForecaster(window=5)
    idxs = list(range(0, 100, 10))

    for model in MODELS:
        rows = results.get(model, [])
        done = {r["i"] for r in rows}
        if len(done) == len(idxs):
            print(f"skip {model}", flush=True)
            continue
        for i in idxs:
            if i in done:
                continue
            state = states[i]
            obs = {"t": i, "slices": {s: {
                "load": state[s], "replicas": 1,
                "delay": cm.delay(state[s], 1, cfgs[s]),
                "loss": cm.loss(state[s], 1, cfgs[s]),
            } for s in cm.SLICES}}
            history = list(agg[:i + 1])
            f = fc.predict(history)
            pv = violation_prob(float(predictor.predict([f])[0]), agg_nf.delay_budget)
            payload = build_payload(obs, f, pv, cfgs)
            try:
                r = call_llm_with_tools(model, payload, cfgs,
                                        ["inspect_infrastructure", "scale_replicas"])
                rec = {"i": i, "actions": r["actions"], "trace": r.get("trace", [])}
                rows.append(rec)
                results[model] = rows
                json.dump(results, open(OUT, "w"), indent=1)
                print(f"  {model} i={i}: {len(rec['trace'])} tool calls", flush=True)
            except Exception as e:
                print(f"  miss {model} i={i}: {type(e).__name__}", flush=True)
            time.sleep(5)

    for model in MODELS:
        rows = results.get(model, [])
        if not rows:
            continue
        print(f"\n=== {model} (sample i={rows[0]['i']}) ===")
        for tc in rows[0]["trace"]:
            print(f"  {tc['name']}({json.dumps(tc['args'])})")
            print(f"      -> {json.dumps(tc['result'])}")
        print(f"  final actions: {rows[0]['actions']}")


if __name__ == "__main__":
    raise SystemExit(main())

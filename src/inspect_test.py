"""A/B: inspect_infrastructure tool vs no tool (resumable, rate-tolerant).

Measures over/under/mae vs required_replicas(load), and records which tools
each model actually called (tools_used) for the analysis.
"""
import json
import os
import time
from collections import Counter

import numpy as np

from . import benchmark as bench
from . import capacity_model as cm
from .dataset import load_result_dir, sorted_by_load
from .kpi_predictor import MLPRegressor, violation_prob
from .forecaster import LinearForecaster
from .llm_compiler import build_payload, call_llm_model, call_llm_with_tools

MODELS = ["glm-5.3-flash:cloud", "deepseek-v4-pro:cloud", "glm-5.3:cloud"]
OUT = os.path.join(bench.REPO_ROOT, "results", "inspect_test.json")


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
        for arm in ["no-tool", "inspect"]:
            key = f"{model}|{arm}"
            rows = results.get(key, [])
            done = {r["i"] for r in rows}
            if len(done) == len(idxs):
                print(f"skip {key}", flush=True)
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
                    if arm == "no-tool":
                        r = call_llm_model(model, payload, cfgs)
                        tools = []
                    else:
                        r = call_llm_with_tools(model, payload, cfgs,
                                                ["inspect_infrastructure", "scale_replicas"])
                        tools = r.get("tools_used", [])
                    rec = {"i": i, "over": 0.0, "under": 0.0, "mae": 0.0,
                           "tools_used": tools}
                    for s in cm.SLICES:
                        req = cm.required_replicas(state[s], cfgs[s])
                        a = r["actions"][s]
                        rec["over"] += max(0, a - req)
                        rec["under"] += max(0, req - a)
                        rec["mae"] += abs(a - req)
                    for k in ("over", "under", "mae"):
                        rec[k] /= 3
                    rows.append(rec)
                    results[key] = rows
                    json.dump(results, open(OUT, "w"), indent=1)
                    print(f"  {key} i={i} done", flush=True)
                except Exception as e:
                    print(f"  miss {key} i={i}: {type(e).__name__}", flush=True)
                time.sleep(5)

    print(f"\n{'model':22} {'arm':8} {'over':>6} {'under':>6} {'mae':>6}  tools")
    for model in MODELS:
        for arm in ["no-tool", "inspect"]:
            key = f"{model}|{arm}"
            rows = results.get(key, [])
            if not rows:
                print(f"{model:22} {arm:8} -- incomplete --")
                continue
            over = float(np.mean([r["over"] for r in rows]))
            under = float(np.mean([r["under"] for r in rows]))
            mae = float(np.mean([r["mae"] for r in rows]))
            tc = Counter(t for r in rows for t in r.get("tools_used", []))
            tstr = " ".join(f"{t}={c}" for t, c in tc.items()) or "-"
            print(f"{model:22} {arm:8} {over:6.2f} {under:6.2f} {mae:6.2f}  {tstr}  (n={len(rows)})")


if __name__ == "__main__":
    raise SystemExit(main())

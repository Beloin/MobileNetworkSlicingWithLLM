"""Inspect-tool A/B across all 3 scenarios, 3 fast models (mistral excluded).

Resumable, rate-tolerant. Records over/under/mae + tools_used per decision.
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
OUT = os.path.join(bench.REPO_ROOT, "results", "inspect_scenarios.json")


def scenarios(states):
    srt = sorted(range(len(states)), key=lambda i: sum(states[i].values()))
    ordered = [states[i] for i in srt]
    low, high = ordered[:40], ordered[80:]
    return {"ramp": ordered,
            "steady": ordered[30:70] * 2,
            "spike": low[:20] + high[:10] + low[20:40] + high[10:20] + low[:20]}


def sample(sstates, n=10):
    step = max(1, len(sstates) // n)
    return sstates[::step][:n]


def main():
    results = json.load(open(OUT)) if os.path.exists(OUT) else {}

    states, delays, losses = load_result_dir(bench.DEFAULT_DIR)
    states, delays, losses = sorted_by_load(states, delays, losses)
    cfgs = bench.build_cfgs(states, delays)
    agg_nf = bench.build_agg_nf(states, delays)
    agg = [sum(s.values()) for s in states]
    predictor = MLPRegressor().fit(agg, delays)
    fc = LinearForecaster(window=5)
    scens = scenarios(states)

    for scen, sstates in scens.items():
        sub = sample(sstates, 10)
        for model in MODELS:
            for arm in ["no-tool", "inspect"]:
                key = f"{scen}|{model}|{arm}"
                rows = results.get(key, [])
                done = {r["k"] for r in rows}
                if len(done) == len(sub):
                    print(f"skip {key}", flush=True)
                    continue
                for k, state in enumerate(sub):
                    if k in done:
                        continue
                    obs = {"t": k, "slices": {s: {
                        "load": state[s], "replicas": 1,
                        "delay": cm.delay(state[s], 1, cfgs[s]),
                        "loss": cm.loss(state[s], 1, cfgs[s]),
                    } for s in cm.SLICES}}
                    hist = [sum(state.values())]
                    f = fc.predict(hist)
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
                        rec = {"k": k, "over": 0.0, "under": 0.0, "mae": 0.0,
                               "tools_used": tools}
                        for s in cm.SLICES:
                            req = cm.required_replicas(state[s], cfgs[s])
                            a = r["actions"][s]
                            rec["over"] += max(0, a - req)
                            rec["under"] += max(0, req - a)
                            rec["mae"] += abs(a - req)
                        for kk in ("over", "under", "mae"):
                            rec[kk] /= 3
                        rows.append(rec)
                        results[key] = rows
                        json.dump(results, open(OUT, "w"), indent=1)
                        print(f"  {key} k={k} done", flush=True)
                    except Exception as e:
                        print(f"  miss {key} k={k}: {type(e).__name__}", flush=True)
                    time.sleep(5)

    for scen in ["ramp", "steady", "spike"]:
        print(f"\n[{scen}]")
        print(f"  {'model':22} {'arm':8} {'over':>5} {'under':>6} {'mae':>5}  tools")
        for model in MODELS:
            for arm in ["no-tool", "inspect"]:
                key = f"{scen}|{model}|{arm}"
                rows = results.get(key, [])
                if not rows:
                    print(f"  {model:22} {arm:8} -- incomplete --")
                    continue
                over = float(np.mean([r["over"] for r in rows]))
                under = float(np.mean([r["under"] for r in rows]))
                mae = float(np.mean([r["mae"] for r in rows]))
                tc = Counter(t for r in rows for t in r.get("tools_used", []))
                tstr = " ".join(f"{t}={c}" for t, c in tc.items()) or "-"
                print(f"  {model:22} {arm:8} {over:5.2f} {under:6.2f} {mae:5.2f}  {tstr} (n={len(rows)})")


if __name__ == "__main__":
    raise SystemExit(main())

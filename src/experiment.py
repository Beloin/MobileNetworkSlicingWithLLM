"""Run scenarios + real LLM experiments, dump JSON to results/.

Usage: python -m src.experiment [result_dir]
"""
import os
import sys
import json
import numpy as np

from . import capacity_model as cm
from .dataset import load_result_dir, sorted_by_load
from .kpi_predictor import MLPRegressor, violation_prob
from .forecaster import LinearForecaster
from . import benchmark as bench
from .llm_compiler import build_payload, call_llm_model
from .mcp_server import call_tool


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
MODELS = ["glm-5.3-flash:cloud", "glm-5.3:cloud",
          "mistral-large-4:cloud", "deepseek-v4-pro:cloud"]


def scenarios(states):
    srt = sorted(range(len(states)), key=lambda i: sum(states[i].values()))
    ordered = [states[i] for i in srt]
    ramp = ordered
    steady = ordered[30:70] * 2
    low, high = ordered[:40], ordered[80:]
    spike = low[:20] + high[:10] + low[20:40] + high[10:20] + low[:20]
    return {"ramp": ramp, "steady": steady, "spike": spike}


def make_obs(state, cfgs):
    return {"t": 0, "slices": {s: {
        "load": state[s],
        "replicas": cfgs[s].min_replicas,
        "delay": cm.delay(state[s], cfgs[s].min_replicas, cfgs[s]),
        "loss": cm.loss(state[s], cfgs[s].min_replicas, cfgs[s]),
    } for s in cm.SLICES}}


def main():
    result_dir = sys.argv[1] if len(sys.argv) > 1 else bench.DEFAULT_DIR
    states, delays, losses = load_result_dir(result_dir)
    states, delays, losses = sorted_by_load(states, delays, losses)
    cfgs = bench.build_cfgs(states, delays)
    agg_nf = bench.build_agg_nf(states, delays)
    agg = [sum(st.values()) for st in states]
    predictor = MLPRegressor().fit(agg, delays)

    results = {"benchmark": {}, "llm": {}, "mcp": {}}

    methods = bench.make_methods(cfgs, agg_nf, predictor)
    for name, states_s in scenarios(states).items():
        results["benchmark"][name] = {}
        for mname, decide in methods.items():
            out = bench.run_method(states_s, cfgs, decide)
            results["benchmark"][name][mname] = bench.metrics(out)

    # Real-LLM closed loop over a reduced ramp subset (fair comparison on the
    # same 34 states). Uses the fast model to bound wall-clock.
    subset = scenarios(states)["ramp"][::3]
    results["benchmark"]["ramp-llm"] = {}
    for mname, decide in methods.items():
        out = bench.run_method(subset, cfgs, decide)
        results["benchmark"]["ramp-llm"][mname] = bench.metrics(out)
    fc2 = LinearForecaster(window=5)

    def real_decide(obs, history):
        fc = fc2.predict(history)
        pv = violation_prob(float(predictor.predict([fc])[0]), agg_nf.delay_budget)
        payload = build_payload(obs, fc, pv, cfgs)
        r = call_llm_model("glm-5.3-flash:cloud", payload, cfgs)
        return r["actions"]

    out = bench.run_method(subset, cfgs, real_decide)
    results["benchmark"]["ramp-llm"]["llm-real-flash"] = bench.metrics(out)
    print("[llm] closed loop: glm-5.3-flash:cloud over 34 states done")

    results["mcp"] = {
        "estimate_capacity": call_tool("estimate_capacity",
                                       {"slice_type": "URLLC", "load_mbps": 200.0}, cfgs),
        "scale_replicas_ok": call_tool("scale_replicas",
                                       {"slice_type": "URLLC", "replicas": 3}, cfgs),
        "scale_replicas_bad": call_tool("scale_replicas",
                                        {"slice_type": "URLLC", "replicas": 99}, cfgs),
        "add_nf_instance": call_tool("add_nf_instance",
                                     {"slice_type": "eMBB", "region": "edge-1"}, cfgs),
    }

    idxs = [10, 40, 70, 90]
    for model in MODELS:
        results["llm"][model] = []
        for k, i in enumerate(idxs):
            obs = make_obs(states[i], cfgs)
            fc = float(agg[i])
            pv = violation_prob(float(predictor.predict([fc])[0]), agg_nf.delay_budget)
            payload = build_payload(obs, fc, pv, cfgs)
            try:
                r = call_llm_model(model, payload, cfgs)
                rec = {"call": k + 1, "state_index": i, "actions": r["actions"],
                       "reason": r["reason"], "latency_ms": round(r["latency_ms"], 1),
                       "usage": r["usage"]}
            except Exception as e:
                rec = {"call": k + 1, "state_index": i,
                       "error": f"{type(e).__name__}: {e}"}
            results["llm"][model].append(rec)
            if "error" in rec:
                print(f"[llm] {model} call {k + 1}: {rec['error']}")
            else:
                print(f"[llm] {model} call {k + 1}: {rec['actions']} "
                      f"{rec['latency_ms']}ms")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, "experiment_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nwrote {out_path}\n")

    for scen, mm in results["benchmark"].items():
        print(f"[{scen}]")
        for m, met in mm.items():
            print(f"  {m:22} viol%={met['viol%']:5.1f} repl={met['avg_replicas']:4.2f} "
                  f"under={met['under']:4.2f} over={met['over']:4.2f} mae={met['mae']:4.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

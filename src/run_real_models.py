"""Run the other 3 cloud LLMs over the 34-state ramp subset, merge into results.

Adds llm-glm5.3 / llm-mistral / llm-deepseek to results["benchmark"]["ramp-llm"]
and renames llm-real-flash -> llm-flash for a consistent 4-model table.
"""
import os
import json
import time

from . import benchmark as bench
from .dataset import load_result_dir, sorted_by_load
from .kpi_predictor import MLPRegressor, violation_prob
from .forecaster import LinearForecaster
from .llm_compiler import build_payload, call_llm_model

MODELS = {"glm-5.3:cloud": "llm-glm5.3",
          "mistral-large-4:cloud": "llm-mistral",
          "deepseek-v4-pro:cloud": "llm-deepseek"}


def main():
    states, delays, losses = load_result_dir(bench.DEFAULT_DIR)
    states, delays, losses = sorted_by_load(states, delays, losses)
    cfgs = bench.build_cfgs(states, delays)
    agg_nf = bench.build_agg_nf(states, delays)
    agg = [sum(s.values()) for s in states]
    predictor = MLPRegressor().fit(agg, delays)
    fc = LinearForecaster(window=5)
    subset = states[::3]  # 34 states, same as ramp-llm

    path = os.path.join(bench.REPO_ROOT, "results", "experiment_results.json")
    with open(path) as fh:
        res = json.load(fh)
    for scen in ["ramp", "ramp-llm"]:
        d = res["benchmark"].get(scen, {})
        if "llm-real-flash" in d:
            d["llm-flash"] = d.pop("llm-real-flash")

    for model, key in MODELS.items():
        count = {"n": 0}
        t0 = time.time()

        def decide(obs, history):
            f = fc.predict(history)
            pv = violation_prob(float(predictor.predict([f])[0]), agg_nf.delay_budget)
            payload = build_payload(obs, f, pv, cfgs)
            r = call_llm_model(model, payload, cfgs)
            count["n"] += 1
            if count["n"] % 10 == 0:
                print(f"  [{key}] {count['n']}/{len(subset)} ({time.time()-t0:.0f}s)",
                      flush=True)
            return r["actions"]

        out = bench.run_method(subset, cfgs, decide)
        m = bench.metrics(out)
        res["benchmark"]["ramp-llm"][key] = m
        print(f"{key}: viol%={m['viol%']:.1f} repl={m['avg_replicas']:.2f} "
              f"under={m['under']:.2f} over={m['over']:.2f} mae={m['mae']:.2f} "
              f"({time.time()-t0:.0f}s)", flush=True)

    with open(path, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"wrote {path}", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())

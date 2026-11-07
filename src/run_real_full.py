"""Run the fast real LLM over the FULL ramp loop (100 states) and merge into
results JSON, alongside the other methods on the same 100 states."""
import os
import json
import time

from . import benchmark as bench
from .dataset import load_result_dir, sorted_by_load
from .kpi_predictor import MLPRegressor, violation_prob
from .forecaster import LinearForecaster
from .llm_compiler import build_payload, call_llm_model

MODEL = "glm-5.3-flash:cloud"


def main():
    states, delays, losses = load_result_dir(bench.DEFAULT_DIR)
    states, delays, losses = sorted_by_load(states, delays, losses)
    cfgs = bench.build_cfgs(states, delays)
    agg_nf = bench.build_agg_nf(states, delays)
    agg = [sum(s.values()) for s in states]
    predictor = MLPRegressor().fit(agg, delays)
    fc = LinearForecaster(window=5)
    count = {"n": 0}
    t0 = time.time()

    def decide(obs, history):
        f = fc.predict(history)
        pv = violation_prob(float(predictor.predict([f])[0]), agg_nf.delay_budget)
        payload = build_payload(obs, f, pv, cfgs)
        r = call_llm_model(MODEL, payload, cfgs)
        count["n"] += 1
        if count["n"] % 10 == 0:
            print(f"  step {count['n']}/{len(states)}  ({time.time()-t0:.0f}s)")
        return r["actions"]

    out = bench.run_method(states, cfgs, decide)
    m = bench.metrics(out)

    path = os.path.join(bench.REPO_ROOT, "results", "experiment_results.json")
    with open(path) as fh:
        res = json.load(fh)
    res["benchmark"]["ramp"]["llm-real-flash"] = m
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2)

    print(f"llm-real-flash (full ramp, {len(states)} states): "
          f"viol%={m['viol%']:.1f} repl={m['avg_replicas']:.2f} "
          f"under={m['under']:.2f} over={m['over']:.2f} mae={m['mae']:.2f}")
    print(f"wrote {path}")


if __name__ == "__main__":
    raise SystemExit(main())

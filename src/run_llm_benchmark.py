"""Run the closed-loop LLM (tool-calling) for all 3 models over ALL scenarios
(ramp 100 + steady 80 + spike 80) and merge into benchmark[scenario].

Adds llm-flash / llm-glm5.3 / llm-deepseek to each scenario. Removes the old
redundant ramp-llm subset scenario and its stale plain-JSON flash row.
Resumable per (scenario, model).
"""
import json
import os
import time

from . import benchmark as bench
from .dataset import load_result_dir, sorted_by_load
from .kpi_predictor import MLPRegressor, violation_prob
from .forecaster import LinearForecaster
from .llm_compiler import build_payload, call_llm_with_tools

MODELS = {"glm-5.3-flash:cloud": "llm-flash",
          "glm-5.3:cloud": "llm-glm5.3",
          "deepseek-v4-pro:cloud": "llm-deepseek"}
TOOLS = ["inspect_infrastructure", "scale_replicas"]


def scenarios(states):
    # states already sorted by load
    ordered = states
    low, high = ordered[:40], ordered[80:]
    return {"ramp": ordered,
            "steady": ordered[30:70] * 2,
            "spike": low[:20] + high[:10] + low[20:40] + high[10:20] + low[:20]}


def main():
    states, delays, losses = load_result_dir(bench.DEFAULT_DIR)
    states, delays, losses = sorted_by_load(states, delays, losses)
    cfgs = bench.build_cfgs(states, delays)
    agg_nf = bench.build_agg_nf(states, delays)
    agg = [sum(s.values()) for s in states]
    predictor = MLPRegressor().fit(agg, delays)
    fc = LinearForecaster(window=5)
    scen_states = scenarios(states)

    path = os.path.join(bench.REPO_ROOT, "results", "experiment_results.json")
    res = json.load(open(path))
    res["benchmark"].pop("ramp-llm", None)  # redundant now that LLM is in ramp
    json.dump(res, open(path, "w"), indent=2)

    t_all = time.time()
    for scen, sstates in scen_states.items():
        bench_scen = res["benchmark"].setdefault(scen, {})
        for model, label in MODELS.items():
            if label in bench_scen:
                print(f"skip {scen}|{label}", flush=True)
                continue
            count = {"n": 0}
            t0 = time.time()

            def decide(obs, history):
                f = fc.predict(history)
                pv = violation_prob(float(predictor.predict([f])[0]), agg_nf.delay_budget)
                payload = build_payload(obs, f, pv, cfgs)
                r = call_llm_with_tools(model, payload, cfgs, TOOLS)
                count["n"] += 1
                if count["n"] % 10 == 0:
                    dt = time.time() - t0
                    print(f"  {scen}|{label} step {count['n']}/{len(sstates)} "
                          f"({dt:.0f}s, {dt/count['n']:.1f}s/step)", flush=True)
                time.sleep(5)  # space out POSTs to stay under rate limits
                return r["actions"]

            out = bench.run_method(sstates, cfgs, decide)
            bench_scen[label] = bench.metrics(out)
            json.dump(res, open(path, "w"), indent=2)
            m = bench_scen[label]
            print(f"{scen}|{label}: viol%={m['viol%']:.1f} repl={m['avg_replicas']:.2f} "
                  f"under={m['under']:.2f} over={m['over']:.2f} mae={m['mae']:.2f} "
                  f"({time.time()-t0:.0f}s)", flush=True)
            time.sleep(2)

    json.dump(res, open(path, "w"), indent=2)
    print(f"wrote {path} ({time.time()-t_all:.0f}s total)", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())

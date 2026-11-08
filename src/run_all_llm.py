"""Run all 4 cloud LLMs over all scenarios (full length), merge into results.

Fills ramp/steady/spike with llm-flash / llm-glm5.3 / llm-mistral / llm-deepseek
at full state counts. Skips keys already present (resumable). Removes the
34-state ramp-llm table.
"""
import os
import json
import time

from . import benchmark as bench
from .dataset import load_result_dir, sorted_by_load
from .kpi_predictor import MLPRegressor, violation_prob
from .forecaster import LinearForecaster
from .llm_compiler import build_payload, call_llm_model

MODELS = {"glm-5.3-flash:cloud": "llm-flash",
          "glm-5.3:cloud": "llm-glm5.3",
          "mistral-large-4:cloud": "llm-mistral",
          "deepseek-v4-pro:cloud": "llm-deepseek"}


def scenarios(states):
    srt = sorted(range(len(states)), key=lambda i: sum(states[i].values()))
    ordered = [states[i] for i in srt]
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
    scens = scenarios(states)

    path = os.path.join(bench.REPO_ROOT, "results", "experiment_results.json")
    with open(path) as fh:
        res = json.load(fh)
    res["benchmark"].pop("ramp-llm", None)
    if "llm-real-flash" in res["benchmark"].get("ramp", {}):
        res["benchmark"]["ramp"]["llm-flash"] = res["benchmark"]["ramp"].pop("llm-real-flash")

    for scen, sstates in scens.items():
        for model, key in MODELS.items():
            if key in res["benchmark"].get(scen, {}):
                print(f"skip {scen}/{key} (already done)", flush=True)
                continue
            count = {"n": 0}
            t0 = time.time()

            def decide(obs, history):
                f = fc.predict(history)
                pv = violation_prob(float(predictor.predict([f])[0]), agg_nf.delay_budget)
                payload = build_payload(obs, f, pv, cfgs)
                r = call_llm_model(model, payload, cfgs)
                count["n"] += 1
                if count["n"] % 20 == 0:
                    print(f"  [{scen}/{key}] {count['n']}/{len(sstates)} "
                          f"({time.time()-t0:.0f}s)", flush=True)
                return r["actions"]

            out = bench.run_method(sstates, cfgs, decide)
            m = bench.metrics(out)
            res["benchmark"].setdefault(scen, {})[key] = m
            print(f"{scen}/{key}: viol%={m['viol%']:.1f} repl={m['avg_replicas']:.2f} "
                  f"under={m['under']:.2f} over={m['over']:.2f} mae={m['mae']:.2f} "
                  f"({time.time()-t0:.0f}s)", flush=True)
            with open(path, "w") as fh:
                json.dump(res, fh, indent=2)
    print("all done", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())

"""RQ5: does giving the LLM the estimate_capacity tool improve decisions?

Compares the fast cloud model with vs without tool-calling over the same
states. Tool mode routes calls through the MCP server (call_tool).
"""
import os
import json

from . import benchmark as bench
from .dataset import load_result_dir, sorted_by_load
from .kpi_predictor import MLPRegressor, violation_prob
from .forecaster import LinearForecaster
from .llm_compiler import build_payload, call_llm_model, call_llm_with_tools

MODEL = "glm-5.3-flash:cloud"


def main():
    states, delays, losses = load_result_dir(bench.DEFAULT_DIR)
    states, delays, losses = sorted_by_load(states, delays, losses)
    cfgs = bench.build_cfgs(states, delays)
    agg_nf = bench.build_agg_nf(states, delays)
    agg = [sum(s.values()) for s in states]
    predictor = MLPRegressor().fit(agg, delays)
    fc = LinearForecaster(window=5)
    subset = states[::5]  # 20 states

    def signals(obs, history):
        f = fc.predict(history)
        pv = violation_prob(float(predictor.predict([f])[0]), agg_nf.delay_budget)
        return f, pv, build_payload(obs, f, pv, cfgs)

    def decide_no_tool(obs, history):
        f, pv, payload = signals(obs, history)
        return call_llm_model(MODEL, payload, cfgs)["actions"]

    tool_use = {"per_decision": [], "estimate_capacity": 0}

    def decide_tool(obs, history):
        f, pv, payload = signals(obs, history)
        r = call_llm_with_tools(MODEL, payload, cfgs,
                                ["estimate_capacity", "scale_replicas"])
        tool_use["per_decision"].append(r["tools_used"])
        tool_use["estimate_capacity"] += r["tools_used"].count("estimate_capacity")
        return r["actions"]

    m_no = bench.metrics(bench.run_method(subset, cfgs, decide_no_tool))
    m_tool = bench.metrics(bench.run_method(subset, cfgs, decide_tool))

    print(f"RQ5 ({MODEL}, {len(subset)} states):")
    for label, m in [("no-tool", m_no), ("tool   ", m_tool)]:
        print(f"  {label}: viol%={m['viol%']:5.1f} repl={m['avg_replicas']:4.2f} "
              f"mae={m['mae']:4.2f} under={m['under']:4.2f} over={m['over']:4.2f}")
    print(f"  estimate_capacity calls: {tool_use['estimate_capacity']} "
          f"across {len(tool_use['per_decision'])} decisions")
    print(f"  sample tool_calls: {tool_use['per_decision'][:5]}")

    path = os.path.join(bench.REPO_ROOT, "results", "experiment_results.json")
    with open(path) as fh:
        res = json.load(fh)
    res["rq5"] = {"model": MODEL, "states": len(subset),
                  "no_tool": m_no, "tool": m_tool, "tool_usage": tool_use}
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"wrote {path}")


if __name__ == "__main__":
    raise SystemExit(main())

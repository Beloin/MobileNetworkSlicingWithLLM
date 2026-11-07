# Pipeline — step by step

Steps, not a time schedule.

## Runtime pipeline

1. Load a sample from the slicing dataset (`maxAvgLambda` + slice-flow bandwidth).
2. Read the resulting per-slice-flow KPI (delay / jitter / loss).
3. Tier 1: forecaster predicts next-window load.
4. Tier 1: KPI predictor estimates `p_violation` for the next window.
5. Capacity model converts load -> required replicas (`ceil(load / (cap * util))`).
6. Build the payload: slice, `kpi_target`, `kpi_now`, ML signals, cluster state.
7. Tier 2 LLM proposes a K8s change (YAML or typed MCP call).
8. Verification gate checks schema + policy. Reject -> one retry, then fall back.
9. Apply the change. Observe the resulting KPI.
10. Hindsight oracle (offline) scores the decision vs the real future load.

## Build order — status: all done

1. `telemetry_env.py` — dataset reader + Gymnasium wrapper. ✅ (per-slice)
2. `capacity_model.py` — load -> replicas / CPU. ✅ (per-slice configs)
3. `kpi_predictor.py` — ML baseline (load -> delay / loss). ✅ (numpy MLP)
4. `forecaster.py` — next-window load. ✅ (linear)
5. `oracle.py` — greedy P95 hindsight oracle. ✅ (per-slice)
6. `llm_compiler.py` — payload builder + API client + retry. ✅ (real Ollama, 4 models)
7. `gate.py` — schema + policy gate. ✅ (+ manifest gate)
8. `baselines.py` — threshold, HPA, predict-then-threshold. ✅
9. `benchmark.py` — scenarios + all metrics. ✅

Extra modules added: `mcp_server.py` (MCP stdio, 5 typed tools), `experiment.py`
(scenarios + real-LLM driver), `run_real_full.py` (full-ramp real LLM),
`report.py` (PDF), `tests/test_end_to_end.py` (8 passing).

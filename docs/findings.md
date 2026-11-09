# Findings & State — 6G Slicing Two-Tier Control Plane

Consolidated knowledge from the prototype work. Written before a context
compaction so nothing critical is lost.

## Project

Two-tier control plane for 6G network slicing. Tier 1 = fast ML (forecaster +
KPI predictor) plus an analytic capacity model. Tier 2 = an LLM (Ollama cloud)
that decides per-slice replica counts and acts through an MCP server of typed
tools. A verification gate checks every change; a hindsight oracle (offline)
scores decisions.

The whole thing is a **simulation** — the "K8s change" is a number fed to the
analytic capacity model, not a real cluster. No kubectl, no pods, no real KPI
telemetry. The dataset supplies the *load* per sample; the delay/loss/violation
are always recomputed from the capacity model, never measured.

## Dataset

- Source: Farreras et al. 2024, Zenodo doi 10.5281/zenodo.10610616
  ("Generation of a network slicing dataset"). Reader lineage: UPC `datanetAPI.py`.
- Local: `datasets/generation_netwok_slicing_dataset/2.2.1-10kprocessed/results_slicing_WFQ_1000_routing_7800_7899`
  (untarred, 100 samples). `datasets/` is a symlink and is gitignored.
- Each sample = per-slice offered load (Mbps) summed over slice flows, for the
  three slice types `eMBB / URLLC / mMTC`, plus a global delay and loss rate.
- `maxAvgLambda` is constant (18 Mbps), so per-slice bandwidth is the load signal.
- Independent steady-state sims, not a time series. `sorted_by_load` turns them
  into a ramp; `steady` = middle 40 samples x2; `spike` = low/high interleave.

## Components

### Capacity model (analytic, NOT ML) — `src/capacity_model.py`
```
effective_capacity = replicas * cap_per_replica
rho = load / capacity
delay = base_delay / (1 - rho)  if rho < 1 else max_delay
loss  = (load - capacity) / load if overloaded else 0
violation = delay > delay_budget OR loss > loss_budget
required_replicas = ceil(load / (cap * target_util))
```
One `NFConfig` per slice: URLLC tight delay (4x base), eMBB loose (30x base),
mMTC strict loss (0.5%). `cap_per_replica` calibrated from the slice's P95 load,
`base_delay` from the dataset's min delay. This is the ground truth for the env,
the oracle, the gate, the baselines, and the MCP tools.

### Forecaster — `src/forecaster.py`
Linear regression over the last 5 aggregate-load points (or persistence).
Output: `forecast_mbps`.

### KPI predictor — `src/kpi_predictor.py`
Pure-numpy MLP regressor (16 hidden, ReLU, MSE, 3000 epochs) trained on
`aggregate load -> delay`. `p_violation = sigmoid((pred_delay - budget)/budget)`.

### Baselines — `src/baselines.py`
- **threshold**: reactive — scale to required only after a violation; scale down
  below 50% budget.
- **hpa**: ideal controller — always `required_replicas(load)`.
- **predict-then-threshold**: MLP delay prediction then a threshold (degenerates
  to HPA in practice — the MLP over-predicts delay).
- **capacity-rule** (formerly `llm-stub`, code fn `call_stub`): deterministic
  rule. If `p_violation > 0.5` and required > current -> scale to required;
  elif `p_violation < 0.1` and current > min -> scale down one; else hold.
  Shares the capacity model with the oracle, so it is a near-optimal reference.

### LLM — `src/llm_compiler.py`
Ollama cloud models over localhost OpenAI-compatible endpoint
(`http://localhost:11434/v1`, no token), temperature 0.
- `glm-5.3-flash:cloud` (fast), `glm-5.3:cloud`, `deepseek-v4-pro:cloud`.
- `mistral-large-4:cloud` excluded — ~3x slower, ~2x more tokens, same decisions.
- `call_llm_model`: plain JSON prompt (no tools).
- `call_llm_with_tools`: tool-calling harness. **Refactored to tool-call-as-answer**
  — the model's `scale_replicas` calls ARE the answer; no JSON parsing. Returns
  `{actions, tools_used, trace, usage, latency_ms}`.
- `chat()` retries on HTTP 429/5xx and timeouts with backoff.

### MCP server — `src/mcp_server.py`
Six typed tools (JSON-RPC 2.0 over stdio, dependency-free):
- `estimate_capacity(slice, load)` -> required replicas
- `scale_replicas(slice, n)` -> validated/clamped replicas
- `set_resources(slice, cpu, mem)` -> manifest patch (mock)
- `add_nf_instance(slice, region)` -> create (mock)
- `apply_k8s_manifest(id, yaml)` -> validate Deployment manifest
- `inspect_infrastructure(state)` -> per-slice utilization, capacity, headroom,
  required replicas, feasibility, budgets. Accepts dict or JSON string (fixed).

## Key results

### Full closed loop (per-slice) — `results/experiment_results.json`

All controllers run the full ramp/steady/spike. `llm-*` = Ollama cloud LLM
acting through MCP tools (inspect_infrastructure + scale_replicas), 3 models.

```
# ramp (100 states)
method                  viol%  repl  under  over   mae
threshold                24.7  2.50   1.11  0.11  0.49
hpa                      15.7  2.63   0.95  0.08  0.00
predict-then-threshold   15.7  2.63   0.95  0.08  0.00
capacity-rule             1.0  3.73   0.16  0.38  1.10
llm-flash                10.0  3.09   0.74  0.33  0.47
llm-glm5.3                8.0  3.50   0.57  0.57  0.87
llm-deepseek             13.3  2.83   0.86  0.19  0.21

# steady (80 states)
threshold 27.5 / hpa 16.7 / predict 16.7 / capacity-rule 0.8
llm-flash 11.2 / llm-glm5.3 9.2 / llm-deepseek 16.7

# spike (80 states)
threshold 20.0 / hpa 14.6 / predict 15.0 / capacity-rule 1.7
llm-flash 8.3 / llm-glm5.3 5.4 / llm-deepseek 12.1
```

capacity-rule still the best on violation (~1%) — it is a deterministic
over-provisioner (over > under everywhere) that buys headroom via hysteresis, not
by seeing the future (it gets the same payload as the LLM: current load +
forecast + p_violation). The tool-calling LLM beats threshold/hpa but trails
capacity-rule; per-model bias varies (deepseek under-provisions, flash/glm5.3
over-provision).

### Inspect-tool A/B — `results/inspect_scenarios.json`
```
scenario  model      no-tool mae   +inspect mae   +inspect under/over
ramp      flash      0.53         0.07          0.00 / 0.07
ramp      deepseek   0.90         0.10          0.10 / 0.00
ramp      glm-5.3    0.90         0.03          0.00 / 0.03
steady    flash      0.87         0.00          0.00 / 0.00
steady    deepseek   1.17         0.00          0.00 / 0.00
steady    glm-5.3    1.03         0.03          0.00 / 0.03
spike     flash      0.87         0.13          0.07 / 0.07
spike     deepseek   0.90         0.03          0.00 / 0.03
spike     glm-5.3    1.17         0.11          0.00 / 0.11
```
`inspect_infrastructure` collapses MAE to ≤0.13 and under-scaling to ~0 across
every scenario and model; no-tool MAE runs 0.5–1.2. The tool, not the model,
provides the accuracy.

### RQ5 — `estimate_capacity` tool — `results/experiment_results.json` `rq5`
no-tool: viol 3.3%, repl 3.53, mae 1.22. tool: viol 10.0%, repl 2.57, mae 0.22.
MAE and cost drop, violation rises (exact, not safer). The richer
`inspect_infrastructure` is the better tool.

### Prompt A/B (cost wording) — `results/prompt_test.json` — REVERTED
Adding "minimize cost, don't over/under-provision" to the prompt flips over ->
under (mae flat). Text prompting cannot fix accuracy. Reverted to the original
prompt.

### Tool-call traces — `results/tool_trace.json`
Every decision = 1 `inspect_infrastructure` + 3 `scale_replicas` (one per slice),
correct args and results. Confirms the harness is wired correctly.

### LLM latency / tokens (single-shot, 4 calls each, 3 models)
flash 2.8s / 1.2k tokens, glm-5.3 4.6s / 1.3k, deepseek 7.2s / 1.7k.
mistral excluded (was ~22.7s / ~2x tokens, same decisions).

## Research questions — answered

- **RQ1 (valid, safe changes)**: yes, within tested scenarios. Gate enforces
  bounds; traces confirm correct calls; rejections proven in unit tests.
- **RQ2 (under/over vs oracle, closed loop)**: flash over-provisions (over
  0.31–0.36, under 0.70–0.85); glm-5.3 over-provisions (over 0.55–0.85);
  deepseek under-provisions (under 0.81–1.11, over 0.19–0.36). The inspect tool
  does NOT collapse the closed-loop error the way it did in isolated A/B — the
  oracle scores against future load.
- **RQ3 (latency/cost)**: flash 2.8s < glm-5.3 4.6s < deepseek 7.2s; mistral
  excluded (~2x tokens, same decisions).
- **RQ4 (YAML vs MCP)**: both wired, not head-to-head. MCP typed tools are safer.
- **RQ5 (estimate_capacity)**: exact but slightly riskier; inspect tool is better.
- **RQ6 (LLM beats rules)**: tool-calling LLM beats threshold and HPA on
  violation (5.4–16.7 vs 14.6–28.4%) but trails capacity-rule (~1%). The gap vs
  capacity-rule is an over-provisioning policy difference, not information
  asymmetry — capacity-rule sees the same payload.

## Decisions / changes made

- `mistral-large-4` excluded entirely (cost, same decisions).
- `call_llm` renamed `call_stub`; benchmark label `llm-stub` renamed `capacity-rule`.
- `call_llm_with_tools` refactored to tool-call-as-answer (no JSON).
- `inspect_infrastructure` accepts dict or JSON-string state (bug fix).
- System prompt reverted (no cost wording).
- `chat()` retries 429/5xx/timeouts.

## Final results — generated

Final numbers above are the clean re-run (tool-call-as-answer harness, no
mistral). Generated with:

1. `python -m src.experiment` — baselines + single-shot LLM (3 models).
2. `python -m src.run_llm_benchmark` — closed-loop tool-calling LLM, all scenarios.
3. `python -m src.inspect_scenarios` — inspect A/B (record only, not in report).
4. `python -m src.rq5_tool` — RQ5.
5. `python -m src.tool_trace` — traces.
6. `python -m src.report_analysis` — `analysis_results.pdf`.

Old pre-exclusion PDFs kept as `docs/analysis_v1.pdf`,
`docs/initial_results_v1.pdf`.

## Commands

```
python -m pytest tests -q                 # 8 tests
python -m src.experiment                  # benchmark + single-shot LLM calls
python -m src.inspect_scenarios           # inspect A/B (mistral excluded)
python -m src.rq5_tool                    # estimate_capacity A/B
python -m src.tool_trace                  # function-call traces
python -m src.report_full                 # analysis.pdf
python -m src.report                      # initial_results.pdf
.venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/eda.ipynb
.venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/llm_harness.ipynb
```

## Artifacts

- `analysis.pdf` — full report (EDA, KPIs, tools, traces, LLMs, RQ answers).
- `initial_results.pdf` — condensed report.
- `notebooks/eda.ipynb` — EDA + manual pipeline test.
- `notebooks/llm_harness.ipynb` — step-by-step LLM tool-call harness.
- `results/*.json` — all experiment data.
- `docs/architecture.puml/png`, `docs/harness.puml/png` — diagrams.

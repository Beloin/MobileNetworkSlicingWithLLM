# Two-Tier Control Plane for 6G Slicing

Fast ML (Tier 1) + LLM/MCP compiler (Tier 2). Turns ML signals + KPIs + cluster state into verified per-slice Kubernetes changes. Prototype is built and tested end to end.

## Architecture

![Architecture](docs/architecture.png)

Source: `docs/architecture.puml`.

## Loop

1. Load a sample: per-slice offered load (eMBB / URLLC / mMTC) + global delay/loss.
2. Tier 1 (fast ML): forecaster + numpy MLP predict delay and violation probability.
3. Analytic capacity model converts per-slice load -> required replicas.
4. Payload = per-slice KPIs + ML signals + current replicas -> Tier 2 LLM.
5. LLM proposes per-slice replica counts (MCP typed tool, or YAML manifest).
6. Verification gate checks schema + policy, then applies.
7. Hindsight oracle (offline, greedy P95) scores the decision vs future load.

## Dataset

| Dataset | Gives | Backing paper |
|---------|-------|---------------|
| Network slicing dataset | per-slice load -> delay/jitter/loss (10k sims, WFQ) | Farreras et al. 2024, Zenodo 10610616 |

One dataset only. AdapShare (temporal load) and DeepSlice (slice classifier) optional, excluded. OpenRAN too large.

## Results (per-slice closed loop)

Ramp, 100 states (steady and spike in `analysis_results.pdf`):

```
method                  viol%  repl  under  over   mae
threshold                24.7  2.50   1.11  0.11  0.49
hpa                      15.7  2.63   0.95  0.08  0.00
predict-then-threshold   15.7  2.63   0.95  0.08  0.00
capacity-rule             1.0  3.73   0.16  0.38  1.10
llm-flash                10.0  3.09   0.74  0.33  0.47
llm-glm5.3                8.0  3.50   0.57  0.57  0.87
llm-deepseek             13.3  2.83   0.86  0.19  0.21
```

`llm-*` = Ollama cloud LLM acting through MCP tools
(inspect_infrastructure + scale_replicas), same closed loop, 3 models.

- capacity-rule shares the oracle's capacity model, so it is a near-optimal
  upper-bound reference, not a competitor to beat.
- The tool-calling LLM beats threshold/hpa on violation but trails capacity-rule;
  per-model bias varies (flash over-provisions, deepseek under-provisions).

## LLM models (Ollama cloud, localhost, no token)

| Model | mean latency | tokens | notes |
|-------|-------------|--------|-------|
| glm-5.3-flash:cloud | 2.8 s | 1.2k | fast |
| glm-5.3:cloud | 4.6 s | 1.3k | |
| deepseek-v4-pro:cloud | 7.2 s | 1.7k | |

mistral-large-4:cloud excluded — ~3x slower, ~2x tokens, same decisions.

## Repo layout

```
src/            # prototype (env, capacity, oracle, gate, mcp_server, llm, benchmark, experiment, report)
tests/          # pytest, 8 passing
results/        # experiment_results.json + graphs
analysis_results.pdf
docs/           # findings, paper-writing guide, PDFs v1/v2, diagrams
PLAN.md         # full plan + findings (section 15)
timeline.md     # pipeline steps
```

## Commands

```
python -m pytest tests -q
python -m src.experiment          # baselines + single-shot LLM -> results JSON
python -m src.run_llm_benchmark   # closed-loop tool-calling LLM, all scenarios
python -m src.report_analysis     # build analysis_results.pdf
python -m src.mcp_server          # serve MCP over stdio
```

## Status

End to end done. RQ5 answered: `estimate_capacity` tool cuts MAE 1.22->0.22 and cost 3.53->2.57 but raises violation 3.3%->10.0% (exact, not safer); `inspect_infrastructure` is the preferred tool. See `analysis_results.pdf` and PLAN.md §15.

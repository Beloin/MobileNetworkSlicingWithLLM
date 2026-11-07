# MERGED PLAN: Two-Tier Control Plane for 6G Slicing (Fast ML/DRL + LLM/MCP Infrastructure Compiler)

This document merges two drafts:
- **v1** = `PLAN.md` (conversation plan: LLM as decision-maker, hindsight oracle, metrics, pitfalls).
- **v2** = uploaded `plan.md` (dual-tier architecture, PPO baseline, FastMCP, verification gates, datasets, roadmap).

Items marked **[verify]** must be checked before they go into the paper.

---

## 1. Core idea

Existing, proven ML/DL models (including reinforcement learning) run **fast** over a dataset replayed row by row and output numeric slicing signals (load forecasts, violation probabilities, slice-share actions). An **LLM** receives those signals together with the KPIs and the **current infrastructure state**, and turns them into concrete Kubernetes changes (more replicas, more CPU, more NFV instances) on the *existing* deployment, through YAML edits or typed MCP functions. A runtime **verification gate** checks every change before it touches the cluster.

```
dataset (row-by-row replay)
  -> Tier 1: fast ML/DRL models (forecast, violation classifier, PPO policy)
  -> consolidated payload (signals + KPIs + uncertainty + current cluster state)
  -> Tier 2: LLM (small local or commercial)
  -> K8s change (YAML diff or MCP function call)
  -> verification gate (schema, fidelity, policy, optional sandbox)
  -> apply -> observe KPI
```

Why two tiers: DRL/classical ML give fast numeric decisions but stop at numbers; LLM agents translate intent into manifests but are slow for the fast loop. Keep the fast loop in Tier 1 and call Tier 2 only when scaling or reconfiguring infrastructure is needed.

## 2. The key design decision: two roles for the LLM

The two drafts implicitly gave the LLM different jobs. Make this explicit and evaluate both:

- **Mode T (Translator):** the LLM must faithfully compile the Tier 1 output into a valid K8s change. Tier 1 is treated as correct. Success = valid, faithful, safe manifest.
- **Mode D (Decider):** the LLM receives signals + KPIs + state and may **disagree** with Tier 1 (e.g., avoid scaling too much or too little when signals conflict or are uncertain). Success = decision matches what was actually needed in hindsight.

Two evaluation tracks follow: **fidelity** (Mode T, verification gate and MAE) and **decision quality** (Mode D, hindsight oracle). Do not mix them: a faithful LLM can still faithfully execute a wrong ML suggestion.

## 3. Terminology (to avoid the "Oracle" collision)

- **Verification gate** (runtime): checks the LLM's proposed change before applying it.
- **Hindsight oracle** (offline): uses the real future demand from the replayed dataset to decide what was actually needed. Used only for evaluation, never visible to the system.

## 4. Contributions and research questions

**Contributions**
1. The LLM writes the K8s changes as a delta over existing state.
2. Evaluation of whether the LLM understands ML outputs and KPIs and makes its own decisions without scaling too much or too little.
3. A reproducible methodology: hindsight oracle, deterministic and non-LLM baselines, decision/fidelity/outcome metrics.
4. Free-form YAML vs. typed MCP functions for changing existing infrastructure.
5. When is an LLM worth using vs. a threshold state machine, the Kubernetes HPA, and an RL policy?

**Research questions**
- RQ1: Can the LLM turn ML outputs + KPIs + state into valid, safe K8s changes? (Mode T)
- RQ2: How often does it under-scale or over-scale relative to the hindsight oracle? (Mode D)
- RQ3: Small local LLM vs. commercial LLM: accuracy, latency, cost, consistency.
- RQ4: YAML vs. MCP functions: safety and accuracy.
- RQ5: Does an `estimate_capacity` tool improve decisions?
- RQ6: In which scenarios does the LLM beat simple rules?

## 5. Related work and gap

Verified in this conversation (read or confirmed via search):

| Work | What it does | Relation to ours |
|---|---|---|
| **AutoRAN** (Maxenti et al., arXiv 2504.11233) | Intent-driven, zero-touch provisioning of open cellular networks on OpenShift, via CI/CD/GitOps (ArgoCD, Tekton), infrastructure-as-code | Day-0/1 provisioning; not an ML-signal-to-scaling loop. Complementary. |
| **Agentic AI Control Plane for 6G Slice Orchestration** (Bandara et al., arXiv 2602.13227) | Fine-tuned LLMs (Qwen2 + LoRA) generate K8s manifests from slice specs; LLM consortium + reasoning validator; MCP validation | Closest on LLM -> K8s manifest. No ML models over a dataset feeding the LLM; little quantitative evaluation. |
| **LLMs meet Network Slicing MANO** (arXiv 2403.13721) | LLM agents generate NSD/VNFD/TOSCA YAML | Intent-driven; no ML layer. |
| **Conflict-Aware Autonomous Resource Orchestration** (arXiv 2610.14903) | Two-timescale: LLM outside the fast loop, deterministic agents per slice | Same separation of fast vs. LLM loop. |
| **Evolving Inspectable O-RAN Slicing xApps with LLMs** (arXiv 2609.27337) | LLM evolves slicing controllers as compact programs | Different output (controller code). |
| **LLM-xApp** | LLM in the RRM loop of O-RAN slicing | LLM in the fast loop (we avoid that). |
| **Toward Semantic Translation in Network Slicing** (Zenodo 20307396) | LLM-based slice configuration | Config generation; no ML signals. |

From draft v2, **not verified** here: AgentRAN, SliceOps, Ferrag et al. (arXiv:2605.01546), Hikmat & Sahib (2026), Alnaim & Alwakeel (2026), Rezazadeh et al. CS-AC, the generative-RL/diffusion slicing paper **[verify all]**.

**Gap:** no work found that combines (a) fast ML/DRL models over a replayed dataset, (b) an LLM interpreting their numeric outputs + KPIs + current cluster state, (c) incremental K8s changes via typed functions, and (d) quantitative evaluation against a hindsight oracle and non-LLM baselines.

**Positioning caution:** AutoRAN is about provisioning, so comparing "control loop latency" with it is apples-to-oranges. Present it as complementary (it deploys the stack; we adapt it at runtime). The search was not exhaustive; re-check IEEE Xplore and Google Scholar before submission, including newer work from the group behind 2602.13227.

**TODO (author):** related-work table along: input type, ML models, LLM role, output type (YAML/calls), state awareness, verification, baselines, metrics, testbed.

## 6. System design

### 6.1 Tier 1: fast ML/DRL
- Reuse published models; training new ones is optional.
- Candidates: load forecaster (LSTM/XGBoost), SLA-violation classifier, **PPO** policy (reference: Hikmat & Sahib 2026 **[verify]**); alternatives: multi-objective PPO / SliceNFV, CS-AC.
- MDP (from v2): state per slice k in {eMBB, URLLC, mMTC}: SINR, buffer occupancy, delay-budget violation, active users, PRB utilization (15-dim). Action: slice shares a_k in [0,1], sum <= 1.
- Report **measured** inference latency; do not assert "<10 ms" as a premise.

### 6.2 Bridge from Tier 1 output to K8s resources
Tier 1 outputs slice shares (a 3-vector, one per slice type) and/or predicted load; a **capacity model** converts them into per-NF targets (replicas, CPU, memory). Who applies the conversion is an experimental variable:
- the LLM does it itself,
- the LLM calls `estimate_capacity`, or
- a deterministic function does it and the LLM only validates/adjusts.

### 6.3 Payload to the LLM
Send a compact summary, not raw rows:

```json
{
  "slice": "urllc-1",
  "kpi_target": {"latency_ms": 10, "loss_pct": 0.01},
  "kpi_now": {"latency_ms": 7.8, "loss_pct": 0.004},
  "ml": {
    "forecast_mbps": {"p50": 820, "low": 760, "high": 890},
    "p_violation_3win": 0.81,
    "rl_suggestion": {"action": "scale_up_upf", "delta": 1, "conf": 0.64}
  },
  "cluster": {
    "upf": {"replicas": 2, "cpu_req": "2", "cpu_util": 0.78},
    "free_cpu": "6",
    "max_replicas": 5
  }
}
```

Include the **current state**: the problem is a delta, it avoids infeasible proposals (beyond cluster capacity) and destructive ones (recreating what runs). Send a summary (replicas, requests/limits, utilization, headroom), not full YAML.

### 6.4 Tier 2: LLM
- Small local LLM (e.g., Llama-3.2-3B or Qwen-2.5-7B via Ollama) vs. a commercial LLM. Fine-tuning optional.
- Optional RAG over 3GPP 5QI / K8s templates.
- Output: YAML change or MCP function call plus a short justification.

### 6.5 Actuation: YAML vs. MCP functions (decide by experiment)

| | Free-form YAML | MCP typed functions |
|---|---|---|
| Safety | Can touch any field | Only what the function exposes |
| Validation | Parse and check afterwards | Schema and limits at call time |
| Auditability | Text diff | Typed action log |
| Flexibility | High | Limited to the catalog |

Candidate functions: `scale_replicas(nf, n)`, `set_resources(nf, cpu, mem)`, `add_nf_instance(type, region)`, `estimate_capacity(load, nf)`, and (from v2) `apply_k8s_manifest(slice_id, yaml)`. Hybrid: the LLM picks calls; the MCP layer validates and generates a patch (Kustomize / `kubectl patch`) while the original YAML stays versioned; roll back if the KPI worsens. Enforce deterministic limits inside the functions.

## 7. Verification gate (runtime)

Run before applying any change; on failure, return the error trace to the LLM for **one** retry, then reject or fall back.

1. **Schema gate:** `kubectl apply --dry-run=server` (preferably; client dry-run validates less) and/or kubeconform / `helm lint`.
2. **Fidelity gate (Mode T only):** parse the proposed change and compute MAE between the LLM's resource values and the intended values from Tier 1: `MAE = (1/M) * sum |V_LLM - V_intended|`; reject if MAE > epsilon. In Mode D this gate is replaced by the decision metrics, since the LLM may legitimately deviate.
3. **Policy gate:** deterministic limits (e.g., URLLC CPU >= 2 cores, total memory <= node capacity, max replicas, allowed namespaces); optionally SHACL, citing 3GPP TS/TR constraints **[verify exact spec references]**.
4. **Sandbox gate (optional):** apply in a digital twin (Gymnasium env, kind cluster, or OpenAirInterface dry-run) and check the KPI.

Do not claim the gate makes changes "100% safe"; claim measured rejection rates and zero unsafe applications **within the tested scenarios**.

## 8. Ground truth for decision quality (offline)

### 8.1 Capacity model
Profile each NF in the testbed (Mbps or sessions per replica at a given CPU). Required replicas = `ceil(predicted load / (capacity per replica * target utilization))`. For latency targets use queueing theory (M/M/c, Erlang-C).

### 8.2 Hindsight oracle
At window `t`, with provisioning delay `d` and horizon `H`:

```python
def oracle(demand, t, current, cap, util=0.7, d=1, H=5, rmin=1, rmax=5):
    fut = demand[t+d : t+d+H]
    req = ceil(np.percentile(fut, 95) / (cap * util))
    req = max(rmin, min(rmax, req))
    label = "up" if req > current else "down" if req < current else "hold"
    return req, label, req - current
```

Use P95 (not max) to avoid noise spikes; scale-down needs hysteresis; report sensitivity to `H`, `d`, utilization.

### 8.3 Optimal trajectory (optional, stronger)
DP or ILP/CP-SAT (OR-Tools): minimize replica cost + SLA-violation penalty + scale-change penalty subject to cluster capacity.

### 8.4 Simulator / digital twin
SimPy (discrete-event) or local K8s (kind) with Open5GS + UERANSIM: apply the action, measure the resulting KPI.

## 9. Data and environment

- Wrap the replay in a `Gymnasium` environment (`NetworkSlicingGymEnv`): `reset()` loads s_0; `step(action)` computes throughput, latency, SLA penalty, emits s_{t+1}. Replay row by row in time steps, which answers "static datasets do not reflect dynamics".
- Resolved datasets (verified against local files under `datasets/`):
  - **AdapShare** (NIST, Gopal et al.): real LTE PRB demand (`Time, NRB`, hourly, ~36 days) + synthetic NR via TimeGAN. Role: temporal load trace for the replay, the Tier-1 forecaster, and the oracle's future demand.
  - **Network slicing dataset** (Farreras et al. 2024, Zenodo doi 10.5281/zenodo.10610616; reader `datanetAPI.py` from UPC): 10k packet-level sims, WFQ slicing, per-slice-flow delay/jitter/loss. Role: load->KPI ground truth for the capacity model and the verification gate.
  - **DeepSlice** (Thantharate et al. 2019, UEMCON): 63,168 rows, 8 categorical inputs (Use Case Type, UE Category, Technology Supported, Day, Time, GBR, Packet Loss Rate, Packet Delay Budget) -> 3 classes {eMBB, URLLC, mMTC}. Role: Tier-1 slice classifier baseline. Correction: it is slice *selection*, NOT flow records and NOT a load->KPI map; 3 classes, no "Master Slice"; no QCI/Duration columns.
- **Mismatch to resolve:** the 15-dim state (SINR, buffer, PRB use) is absent from all three. The slicing dataset is wired/transport (Topology Zoo backbones, WFQ), not RAN. DeepSlice has no temporal dimension. Decide which state variables are simulated and state this openly in the paper.

## 10. Experimental design

**Systems compared:** threshold state machine; Kubernetes HPA (`desiredReplicas = ceil(current * currentMetric / target)`); PPO policy / small supervised classifier (non-LLM AI baseline; the DeepSlice 3-class model fills this slot); small LLM; commercial LLM; each LLM with and without `estimate_capacity`; each with YAML vs. MCP functions; each in Mode T and Mode D.

**Scenarios (hard decisions):** A steady load; B ramp/spike; C conflicting KPIs; D cluster near capacity; E noisy ML outputs or forecast vs. RL disagreement; F wide uncertainty interval.

**Ablations:** raw numbers vs. qualitative labels; with/without RL suggestion; with/without uncertainty; with/without current cluster state; with/without calculator tool.

**Evaluation modes:** *isolated decision* (same state per window for all systems, compare with oracle) and *closed loop* (each system follows its own trajectory in the simulator).

**Repetitions:** N runs per case (e.g., 10) to measure variance; use around 500 test epochs for accuracy metrics.

## 11. Metrics

- **Decision (Mode D):** scale-up recall (missed scale-ups are the key failure of small LLMs), scale-up precision, under-scaling `max(0, req - chosen)`, over-scaling `max(0, chosen - req)`, no-op correctness.
- **Fidelity (Mode T):** manifest compilation accuracy (%), MAE vs. intended values, exact-match rate.
- **Outcome:** SLA/KPI violation rate and duration (windows where demand > chosen * cap), resources vs. minimum required, time to recover KPI.
- **Output quality:** syntactic validity, dry-run acceptance, policy compliance, incremental (non-destructive) changes, gate rejection and retry rates.
- **Latency breakdown (measured):** T_DRL_inference, T_LLM_generation, T_validation, end to end; cost per decision (tokens or USD).
- **Robustness:** variance across runs, sensitivity to payload format and borderline cases near KPI thresholds.

## 12. Pitfalls and threats to validity

- **Leakage:** the future exists only inside the hindsight oracle.
- **Circularity:** if the oracle and `estimate_capacity` share the same capacity model, the LLM with the tool matches the oracle trivially; state it or perturb the model.
- **Trivial ground truth:** if the label is "KPI below threshold -> scale", a state machine scores 100%; use scenarios where rules fall short.
- **Oracle assumptions:** the oracle is a model; document and validate calibration.
- **Non-determinism:** fix model versions and prompts; report variance.
- **Latency claims:** local 3B-7B LLMs generating a manifest typically take far longer than a Tier 1 inference; measure, do not assume "~100 ms".
- **Related-work coverage:** not exhaustive.

## 13. Implementation roadmap

1. `telemetry_env.py`: dataset replay + Gymnasium env; define state variables (Section 9).
2. `drl_engine.py`: PPO (Stable-Baselines3) and/or reuse existing models; lightweight forecaster and violation classifier.
3. `capacity_model.py`: NF profiling, replicas/CPU formulas, queueing model.
4. `oracle.py`: hindsight oracle (greedy and optional ILP) + label generation.
5. `mcp_server.py` (FastMCP): `scale_replicas`, `set_resources`, `add_nf_instance`, `estimate_capacity`, `apply_k8s_manifest`; verification gate embedded.
6. `llm_compiler.py`: payload builder, Ollama / commercial API clients, retry with gate feedback.
7. `baselines.py`: thresholds, HPA, RL policy.
8. `benchmark.py`: scenarios, repetitions, all metrics, latency breakdown.
9. Related-work table and paper.

## 14. Open decisions

- Mode T, Mode D, or both (recommended: both).
- Small and commercial LLMs to use; fine-tune or not.
- YAML vs. MCP functions vs. hybrid.
- Datasets, and which state variables are simulated.
- Oracle variant: greedy vs. optimal trajectory.
- Testbed: SimPy only, or kind + Open5GS + UERANSIM.
- Which Tier 1 models to reuse.

## 15. Implementation status and findings (prototype)

**Status:** end-to-end prototype built and tested. `src/` (per-slice env, capacity model, oracle, gate, MCP server, baselines, LLM compiler, experiment + report). 8 tests passing. Report at `initial_results.pdf`; raw data at `results/experiment_results.json`.

**Resolved decisions:**
- Dataset: slicing dataset only — per-slice offered load (eMBB/URLLC/mMTC) + global delay/loss. AdapShare and DeepSlice excluded for now.
- Oracle: greedy P95 hindsight (prescient, offline only). Not perturbed.
- Testbed: analytic capacity model + Gymnasium-style replay env. No kind/Open5GS.

**Findings (ramp, 100 states, per-slice closed loop):**

| method | viol% | repl | under | over | mae |
|---|---|---|---|---|---|
| threshold | 24.7 | 2.50 | 1.11 | 0.11 | 0.49 |
| hpa | 15.7 | 2.63 | 0.95 | 0.08 | 0.00 |
| predict-then-threshold | 15.7 | 2.63 | 0.95 | 0.08 | 0.00 |
| llm-stub | 1.0 | 3.73 | 0.16 | 0.38 | 1.10 |
| llm-real-flash | 7.7 | 3.93 | 0.53 | 0.96 | 1.48 |

Per RQ:
- **RQ2**: real LLM under-scales 0.53 but over-scales 0.96 — conservative, leaves ~1 replica of headroom. Stub is exact (over 0.38).
- **RQ3**: latencies — glm-5.3-flash 4.4s, deepseek-v4-pro 7.1s, glm-5.3 8.4s, mistral-large-4 22.7s. mistral ~2x tokens, same decisions as the others.
- **RQ4**: both actuation paths wired. MCP typed tools enforce bounds (scale_replicas rejects 99). YAML manifest parsed + gate-checked.
- **RQ5**: with the `estimate_capacity` tool (MCP tool-calling, not plain JSON) the LLM's MAE drops 1.18 -> 0.20 and cost 3.47 -> 2.55 replicas, but violation rises 6.7% -> 11.7% — the tool makes it exact, not safer.
- **RQ6**: real LLM beats threshold (7.7 vs 24.7) and HPA (7.7 vs 15.7) on violation, at higher cost (3.93 vs 2.63 replicas). Stub (exact capacity-model rule) beats all (1.0%).

**Caveats:**
- Only flash ran the full 100-step loop; the other 3 LLMs are single-shot (4 states each).
- Env delay is analytic; dataset delay only calibrates it and trains the MLP.
- Oracle greedy, not ILP. predict-then-threshold degenerates to HPA (MLP over-predicts delay) — needs rework or removal.

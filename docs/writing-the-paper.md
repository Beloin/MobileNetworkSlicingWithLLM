# Writing the Paper: Step-by-Step

A concrete, ordered process for turning this prototype into the thesis/paper.
Every step points to the exact file or artifact that supplies the content, so
you never write from memory — you write from the results.

The paper is a **systems + ML evaluation paper**: it proposes a two-tier
control plane and measures whether an LLM, acting through MCP tools, turns ML
signals + KPIs + cluster state into correct per-slice scaling decisions. The
contribution is the *combination* (fast ML → LLM → MCP → gate → oracle) and the
*quantitative evaluation against non-LLM baselines*.

---

## Main focus of the paper

**One sentence.** This paper evaluates whether an LLM, acting through typed MCP
tools, can compile fast-ML slicing signals + KPIs + current cluster state into
correct, safe per-slice Kubernetes scaling decisions — and measures when that
two-tier design beats non-LLM controllers. The contribution is the
*integration* (fast ML → LLM → MCP → gate → hindsight oracle) plus its
*quantitative evaluation against non-LLM baselines* — not a new ML model, not a
new LLM.

**Where it sits in the thesis.** The thesis (`papers/ufc_network.md`) is titled
"Design of an intelligent orchestration plan for proactive slice management in
6G networks". Its framing: 6G's openness, virtualization, disaggregation and
distributed network functions demand proactive, scalable, interoperable
orchestration of URLLC-critical slices, guided by SLAs and KPIs (QoS/QoE),
through distributed AI and autonomous decision-making. This paper is that
orchestration plan made concrete and measured.

**The two research lines this paper merges.** The project stands on two
literatures; its novelty is putting them in one loop.

1. **Numeric slicing signals + resource allocation (the "fast" tier).**

   - Rodrigues, Vieira, de Castro — "5G Network Slice – A URLLC Resource
     Allocation Perspective" (`papers/5G_Network_Slice___A_URLLC_Resource_AllocationPerspective.pdf`).
     The URLLC slice type this prototype treats as the tight-delay case.
   - Gomes et al. — "Application of Meta-Heuristics in 5G Network Slicing"
     (`papers/sensors-22-06724.pdf`) and "Artificial algae optimization for
     Virtual Network Embedding" (Expert Systems with Applications 2024). The
     optimization/VNE lineage the analytic capacity model replaces with a
     closed form.
   - Gomes et al. — "Network Slicing for Massive Machine Type Communication in
     IoT-5G Scenario" (VTC Spring 2021). The mMTC slice type.
   - DeepSlice (Thantharate 2019), SliceNFV (Alnaim & Alwakeel 2026 **[verify]**),
     CS-AC (Rezazadeh **[verify]**), Hikmat & Sahib PPO **[verify]** — ML/DRL
     slice-class and resource policies (PLAN.md §5–§6).

2. **LLM/MCP as the infrastructure compiler (the "slow" tier).**

   - AutoRAN (Maxenti 2025, arXiv 2504.11233) — zero-touch GitOps-based O-RAN
     provisioning. Complementary: it deploys the stack; ours adapts it at runtime.
   - Bandara et al. — "An Agentic AI Control Plane for 6G Network Slice
     Orchestration" — LLM → K8s manifest with MCP validation. Closest on
     LLM→K8s (arXiv id to verify: 2502.14536 vs 2602.13227).
   - "LLMs meet Network Slicing MANO" (arXiv 2403.13721) — LLM agents generate
     NSD/VNFD/TOSCA YAML.
   - LLM-xApp / "Toward Semantic Translation in Network Slicing" — LLM in the
     RRM loop / slice-config generation.

**The evaluation backbone.** Dataset + ground truth come from Farreras et al.
2024 (Zenodo 10610616; README.md and PLAN.md §9) — per-slice load + global
delay/loss. AdapShare (Gopal/NIST) and DeepSlice are excluded for now. The
hindsight oracle (greedy P95) is the offline decision-quality label.

**What is new (the gap).** No work in `papers/` or PLAN.md §5 combines
(a) fast ML over a replayed dataset, (b) an LLM interpreting numeric outputs +
KPIs + current cluster state, (c) incremental K8s changes through typed MCP
tools, and (d) a quantitative comparison against a hindsight oracle and
non-LLM baselines. That combination is the paper.

**What the paper is NOT (scope guardrails).** Not a new DRL policy (Tier 1
reuses a simple forecast + MLP). Not a new or fine-tuned LLM (Ollama cloud
models, temp 0). Not a live cluster (analytic capacity model, no kubectl/pods).
Not a YAML-vs-MCP head-to-head (both wired; MCP argued safer — RQ4). State each
of these once in the intro so reviewers do not expect the wrong thing.

---

## What is different from prior work

Differentiate on two axes. Reviewers will ask both.

### Axis 1 — vs papers that already use an LLM

AutoRAN, Bandara et al., "LLMs meet Network Slicing MANO", LLM-xApp, "Toward
Semantic Translation", Conflict-Aware Orchestration all use an LLM. The
difference is what feeds the LLM, what it produces, and how it is scored.

| Paper (LLM lineage) | LLM input | LLM output | Evaluation | Our difference |
|---|---|---|---|---|
| AutoRAN (Maxenti 2025) | Intent / infra-as-code | CI/CD, GitOps provisioning | Day-0/1 deploy | We do runtime adaptation, not provisioning |
| Bandara et al. 2025 | Slice spec text | K8s manifest | MCP validation, little quant | We feed numeric ML signals, not spec prose; we score vs oracle |
| LLM-meet-MANO (2403.13721) | Intent | NSD/VNFD/TOSCA YAML | Mostly qualitative | Typed tools + gate + oracle scoring |
| LLM-xApp | RRM loop state | Control decision | — | LLM in the fast loop (we keep ML fast, LLM outside) |
| Toward Semantic Translation | Slice config intent | Config | — | Config generation, no ML-signal loop |
| Conflict-Aware | Two-timescale state | Per-slice deterministic agents | — | Closest framing; we add typed MCP + oracle + baselines |

Four concrete differences:

1. **Input is numeric ML signals + KPIs + current cluster state**, not intent or
   spec prose. They answer "create a URLLC slice"; we answer "here is the
   forecast, p_violation, current replicas and utilization — decide the delta."
2. **Actuation is typed MCP tools under a verification gate**, and every decision
   is scored by an **offline hindsight oracle**. They emit a YAML/manifest; most
   never measure whether the change was right.
3. **Quantitative evaluation**: MAE, under/over-scaling vs oracle, violation %,
   latency, tokens — against **non-LLM baselines**. The LLM papers cited above
   are largely intent-driven demos or provisioning, with little head-to-head
   quantitative comparison.
4. **Two-tier separation**: the LLM stays outside the fast loop and is called
   only for scaling/reconfig. This is the opposite of LLM-xApp's in-loop LLM.

### Axis 2 — vs slicing resource-allocation papers

Rodrigues (URLLC), Gomes et al. (meta-heuristics, algae VNE, mMTC), DeepSlice,
SliceNFV, CS-AC, Hikmat & Sahib (PPO) all optimize slicing — but they are
single-tier and stop at numbers.

1. **They output numbers** (slice share, replica count, class). Ours compiles
   those numbers into **incremental K8s changes** (replicas, CPU/mem, manifests)
   across a typed-tool boundary. The contribution is the translation + safety
   layer, not a new allocator.
2. **They optimize a reward** (sum-rate, delay). Ours adds a **safety/fidelity
   layer** (gate) and measures **decision quality** (under/over vs oracle), not
   just outcome.
3. **They are single-tier**: the ML/DRL model is the whole system. Ours is
   two-tier and explicitly evaluates *when the LLM adds value* (RQ6) — and finds
   the value comes from the MCP inspect tool, not the model. That reframing
   ("the tool, not the LLM, wins") is itself a finding to state, not hide.

### The one-paragraph version (for the intro)

Existing LLM-orchestration work treats the LLM as an intent→YAML compiler with
no numeric ML input and little quantitative scoring; existing slicing work is
single-tier ML/DRL that stops at numbers. This paper is the first to close the
loop: fast ML over a replayed dataset produces numeric signals, the LLM acts on
them through typed MCP tools under a verification gate, and a hindsight oracle
plus non-LLM baselines score every decision — which is also what reveals that the
tool, not the model, is doing the accuracy work.

---

## 0. Read these before you write

| Input | What it gives you |
|---|---|
| `PLAN.md` | Contributions, RQ1–RQ6, system design, gate/oracle spec, threats to validity (§12), implementation findings (§15) |
| `docs/findings.md` | Consolidated component list, all results, RQ answers, decisions |
| `results/experiment_results.json` | Benchmark (threshold/hpa/predict-then-threshold/capacity-rule/llm), single-shot LLM calls, RQ5 |
| `results/inspect_scenarios.json` | Inspect-tool A/B (kept for the record; not in the final report) |
| `results/tool_trace.json` | Full function-call traces (inspect + scale_replicas) |
| `analysis_results.pdf` | Rendered tables + figures + method prose (the merged final report) |
| `papers/reference_matrix.md` | Related-work table + BibTeX |
| `docs/architecture.puml` / `docs/harness.puml` | The two diagrams |

---

## 1. Freeze the numbers first

Do not write prose around numbers that will change. Before drafting:

1. Run the full pipeline (see `docs/findings.md` → "Final real results — generated").
2. Open `analysis_results.pdf`. It is the source of truth for every number you cite.
3. Copy the benchmark table and the RQ5 table into a scratch file. You will
   paste these, nearly verbatim, into the Results section.
4. Note the exact model set: `glm-5.3-flash:cloud`, `glm-5.3:cloud`,
   `deepseek-v4-pro:cloud`. **`mistral-large-4:cloud` is excluded** — ~3×
   slower and ~2× more tokens while returning the same decisions. Say this
   explicitly in the paper; it is a cost/benefit decision, not an omission.

---

## 2. Paper skeleton (map each section to your artifacts)

```
1.  Introduction
2.  Related work
3.  System design            -> PLAN.md §6–§8, src/*, architecture.puml
4.  Experimental setup       -> dataset, scenarios, models, baselines, metrics
5.  Results                  -> results/*.json, RQ1–RQ6, analysis_results.pdf
6.  Discussion / threats     -> PLAN.md §12
7.  Conclusion
```

This is the standard systems-paper shape. Do not deviate — reviewers expect
"design → setup → results → limitations" in exactly this order.

---

## 3. Writing order (do NOT write top to bottom)

Top-to-bottom writing wastes days on the intro that you rewrite later. Use this
order:

**Step 1 — System design (§3).**
Describe what you built, component by component:

- Tier 1: linear forecaster (`src/forecaster.py`) + numpy MLP KPI predictor
  (`src/kpi_predictor.py`).
- Analytic capacity model (`src/capacity_model.py`): the four equations
  (effective_capacity, rho, delay, loss, violation, required_replicas).
- Tier 2: LLM acting through six typed MCP tools (`src/mcp_server.py`).
- Verification gate (`src/gate.py`).
- Hindsight oracle (`src/oracle.py`), greedy P95, offline only.
Put `docs/architecture.png` and `docs/harness.png` here.

**Step 2 — Experimental setup (§4).**

- Dataset: Farreras et al. 2024 (Zenodo 10610616), per-slice load, `maxAvgLambda`
  constant so per-slice bandwidth is the load signal.
- Scenarios: ramp / steady / spike (how each is constructed from
  `sorted_by_load`).
- Baselines: threshold, HPA, predict-then-threshold, capacity-rule, and the LLM.
  Explain what each is and why capacity-rule is an upper-bound reference that
  shares the oracle's model — not a competitor to beat.
- Metrics: violation %, mean replicas, under/over-scaling, recall/precision,
  hold correctness, MAE, latency, tokens. (Why each — copy from the metric
  table in `analysis_results.pdf` §5.)
- Models + how called (Ollama cloud, OpenAI-compatible, temp 0).

**Step 3 — Results (§5), written one RQ at a time.**
Write six subsections, one per RQ. For each: state the question, give the table
or figure, then a 2–3 sentence finding. Do not write narrative first; build the
table/figure first, then write the paragraph that reads it.

**Step 4 — Related work (§2).**
Use `papers/reference_matrix.md`. Structure by row: what each work does, how it
differs. End with the explicit gap (fast ML over a dataset + LLM via typed
tools + quantitative oracle-and-baseline evaluation). Do not over-claim novelty
against AutoRAN — it is provisioning, complementary, not a competitor.

**Step 5 — Introduction (§1).**
Now that sections 3–5 exist, write the intro by answering: what problem, why
two tiers, what you built, what you found (the headline numbers), the
contributions list.

**Step 6 — Abstract.**
Write last. 4 sentences: context, gap, method, headline result.

**Step 7 — Discussion/threats (§6) and Conclusion (§7).**
Threats from PLAN.md §12. Conclusion = contributions + one-sentence RQ answers.

---

## 4. What each RQ claims, and the data that backs it

Copy the *claim*, then paste the *number* from the frozen JSON/PDF. Do not
paraphrase the claim into a weaker or stronger form.

- **RQ1 (valid, safe changes):** Yes, within tested scenarios. Gate enforces
  bounds; `tool_trace.json` confirms correct calls; rejections proven in
  `tests/`. Claim "measured rejection rates", never "100% safe".
- **RQ2 (under/over vs oracle):** Plain LLM over-provisions (over 0.23–1.13
  across scenarios); with `inspect_infrastructure` under+over collapse to ≤0.10.
  Source: benchmark (plain vs tool-calling) — `inspect_scenarios.json` kept for
  the record, not in the final report.
- **RQ3 (latency/cost):** flash 2.8s < glm-5.3 4.6s < deepseek 7.2s; mistral
  ~2× tokens and excluded. Source: `experiment_results.json` → `llm` → `latency_ms` / `usage`.
- **RQ4 (YAML vs MCP):** Both wired, not head-to-head. MCP typed tools are safer
  by construction (bounds at call time). State this as a design argument, not a
  measured comparison.
- **RQ5 (estimate_capacity tool):** no-tool mae 1.22 / repl 3.53 / viol 3.3% →
  tool mae 0.22 / repl 2.57 / viol 10.0% — exact, not safer.
  `inspect_infrastructure` is the better tool. Source: `experiment_results.json` → `rq5`.
- **RQ6 (LLM vs rules):** LLM (tool-calling) beats threshold and HPA on
  violation (8.8 vs 20.6–28.4%) at ~1.4× replica cost; near-optimal with the
  tool. The **tool**, not the model, wins. Source: benchmark table (all scenarios).

---

## 5. Figures and tables to produce (and which code made them)

| Figure/Table | Source | Where in paper |
|---|---|---|
| Architecture diagram | `docs/architecture.png` | §3 |
| Harness diagram | `docs/harness.png` | §3 or §4 |
| Benchmark table (per scenario) | `results/experiment_results.json` → `benchmark` | §5 |
| LLM latency + tokens + per-slice decision | `results/llm.png` (built by `src/report_analysis.py`) | §5 (RQ3) |
| Tool-call trace example | `results/tool_trace.json` (print first row) | §5 (RQ1) |
| RQ5 table | `experiment_results.json` → `rq5` | §5 (RQ5) |

To make a new figure, follow `src/report_analysis.py::make_graphs` — it already
reads the JSON and renders matplotlib. Copy its pattern rather than hand-plotting.

---

## 6. Honesty rules (write these into the prose)

- This is a **simulation**, not a live cluster. No kubectl, no pods, no real
  KPI telemetry — delay/loss/violation are recomputed from the analytic model.
- The **oracle is prescient** and offline-only; never shown to the system.
- The **circularity caveat** (PLAN.md §12): the oracle and `estimate_capacity`
  share the same capacity model, so the tool matching the oracle is partly
  expected. State this; do not hide it.
- Latency numbers are **measured**, not assumed. Report them as-is.
- Non-determinism: fix model versions + prompt, report variance. Temp 0 helps
  but does not guarantee bit-identical runs.

---

## 7. First-draft skeleton (paste and fill)

```markdown
# Title: A Two-Tier Control Plane for 6G Network Slicing: Fast ML + LLM/MCP
#         Infrastructure Compiler

## Abstract
<context> <gap> <method> <headline result, one number>

## 1. Introduction
Problem. Why two tiers. What we built. Headline findings. Contributions (list).

## 2. Related Work
<reference_matrix rows, grouped> -> gap.

## 3. System Design
Tier 1. Capacity model (4 equations). Tier 2 + MCP tools. Gate. Oracle.

## 4. Experimental Setup
Dataset. Scenarios. Baselines (define each). Metrics (table). Models.

## 5. Results
5.1 RQ1 ... 5.6 RQ6, each: claim + table/figure + 2-3 sentence finding.

## 6. Discussion and Threats to Validity
<PLAN.md §12, expanded>

## 7. Conclusion
Contributions + one-sentence RQ answers.
```

---

## 8. Final checklist before you consider it done

- [ ] Every number in the paper matches `results/*.json` (re-run, re-check).
- [ ] Mistral exclusion is stated with the reason.
- [ ] "simulation, not live K8s" is stated once, clearly.
- [ ] Oracle labelled prescient/offline.
- [ ] Circularity caveat present.
- [ ] RQ1 claims "within tested scenarios", not "safe".
- [ ] Related work ends with the explicit gap.
- [ ] Latency values labelled measured, with model version + prompt fixed.
- [ ] Every figure has a caption and is cited in the text.

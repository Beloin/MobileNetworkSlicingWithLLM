"""Generate docs/retrospective.pdf — full project retrospective and lessons
learned: everything found from day one, decisions, what went well/bad, what can
be better, and the capacity-rule cost note."""
import json
import os

import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Preformatted)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
OUT = os.path.join(REPO_ROOT, "docs", "retrospective.pdf")


def _fmt(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "-"
    return f"{x:.2f}"


def load_json(name):
    with open(os.path.join(RESULTS_DIR, name)) as f:
        return json.load(f)


def grid(rows, widths, header=True, font=8):
    t = Table(rows, colWidths=widths)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("FONT", (0, 0), (-1, -1), "Helvetica", font),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]
    if header:
        style += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", font),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9))]
    t.setStyle(TableStyle(style))
    return t


def build_pdf():
    exp = load_json("experiment_results.json")

    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)
    ss = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=17, spaceAfter=6)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=13, spaceBefore=10, spaceAfter=4)
    h3 = ParagraphStyle("h3", parent=ss["Heading3"], fontSize=11, spaceBefore=7, spaceAfter=3)
    body = ParagraphStyle("body", parent=ss["BodyText"], fontSize=9.5, leading=12.5)
    bullet = ParagraphStyle("bullet", parent=body, leftIndent=14, bulletIndent=2, spaceAfter=1)
    mono = ParagraphStyle("mono", parent=ss["Code"], fontSize=8, leading=10, leftIndent=14)

    S = []

    def bl(items):
        for it in items:
            S.append(Paragraph("• " + it, bullet))

    S.append(Paragraph("Prototype Retrospective & Lessons Learned", h1))
    S.append(Paragraph("Two-tier control plane for 6G network slicing (fast ML + LLM/MCP compiler). "
                       "Everything found from day one: what we built, what we chose, what went wrong, "
                       "what went right, and what can be better.", body))
    S.append(Spacer(1, 8))

    # 1. Overview
    S.append(Paragraph("1. What this is", h2))
    S.append(Paragraph("A research prototype for a master's thesis on 6G network slicing. "
                       "Tier 1 runs fast ML (a load forecaster + a numpy MLP KPI predictor) and an "
                       "analytic capacity model; Tier 2 is an LLM (Ollama cloud) that decides per-slice "
                       "replica counts and acts through typed MCP tools; a verification gate checks every "
                       "change; an offline hindsight oracle scores every decision against future load.", body))
    S.append(Paragraph("It is a <b>simulation</b>, not a live cluster. No kubectl, no pods, no real KPI "
                       "telemetry — delay/loss/violation are always recomputed from the analytic capacity "
                       "model, and the dataset supplies only the per-slice load.", body))
    S.append(Spacer(1, 8))

    # 2. Components
    S.append(Paragraph("2. Components", h2))
    S.append(Paragraph("• <b>Capacity model</b> (analytic, not ML) — the shared ground truth for env, "
                       "oracle, gate, baselines and MCP tools:", bullet))
    S.append(Preformatted(
        "effective_capacity = replicas * cap\n"
        "rho = load / capacity\n"
        "delay = base / (1 - rho)  if rho < 1 else max_delay\n"
        "loss  = (load - capacity) / load if overloaded else 0\n"
        "violation = delay > budget OR loss > budget\n"
        "required_replicas = ceil(load / (cap * 0.7))", mono))
    bl([
        "<b>NFConfig per slice</b>: URLLC tight delay, eMBB loose, mMTC strict loss.",
        "<b>Forecaster</b>: linear regression over the last 5 aggregate-load points (or persistence).",
        "<b>KPI predictor</b>: numpy MLP (16 hidden, ReLU, MSE) on aggregate load → delay; "
        "p_violation = sigmoid((pred_delay − budget)/budget).",
        "<b>Baselines</b>: threshold (reactive), hpa (ideal), predict-then-threshold (degenerates to hpa), "
        "capacity-rule (deterministic rule).",
        "<b>MCP server</b>: six typed tools — estimate_capacity, scale_replicas, set_resources, "
        "add_nf_instance, apply_k8s_manifest, inspect_infrastructure.",
        "<b>LLM compiler</b>: OpenAI-compatible tool-calling against Ollama localhost; "
        "tool-call-as-answer (no JSON parsing).",
        "<b>Gate + oracle</b>: verification gate (schema + policy, one retry); hindsight oracle "
        "(greedy future-load P95, offline only).",
    ])
    S.append(Spacer(1, 8))

    # 3. Timeline / what we did
    S.append(Paragraph("3. What we did, in order", h2))
    bl([
        "Interviewed the plan → scope locked: <b>prototype first</b>, 1 month, commercial-API LLM.",
        "Investigated datasets → excluded OpenRAN (too large); kept the Farreras et al. 2024 slicing "
        "dataset (Zenodo 10610616) as the only source.",
        "Considered feeding a DeepSlice-style ML model into the LLM; settled on forecaster + KPI "
        "predictor + analytic capacity model as Tier 1.",
        "Corrected PLAN.md, drew the PlantUML architecture, wrote the papers reference matrix.",
        "Built the end-to-end prototype: dataset → env → capacity model → oracle → gate → MCP → LLM "
        "→ baselines → benchmark → reports.",
        "Generated initial_results.pdf, then expanded analysis.pdf.",
        "Did EDA as a Jupyter notebook (pandas head + manual pipeline walk) and a step-by-step LLM "
        "harness notebook.",
        "Refactored the LLM from JSON output to <b>tool-calling</b> (scale_replicas calls ARE the answer).",
        "Renamed llm-stub → <b>capacity-rule</b> (it is a deterministic rule, not an LLM).",
        "Added the inspect_infrastructure tool and showed (in isolation) it makes the LLM near-exact.",
        "Ran RQ5 (estimate_capacity A/B), tool-call traces, and a prompt A/B (reverted).",
        "Excluded <b>mistral-large-4</b> (too expensive, same decisions).",
        "Ran the full closed-loop LLM benchmark (3 models × ramp/steady/spike) for the final results.",
        "Merged the two reports into a single analysis_results.pdf and wrote this retrospective.",
    ])
    S.append(Spacer(1, 8))

    # 4. Key choices
    S.append(Paragraph("4. Key choices and why", h2))
    bl([
        "<b>Two tiers, LLM outside the fast loop</b>: ML gives fast numeric signals; the LLM is called "
        "only for scaling/reconfig — opposite of putting the LLM in the RRM loop.",
        "<b>Analytic capacity model as ground truth</b>: deterministic, reusable by env, oracle, gate, "
        "baselines and tools. Removes ambiguity about what is 'correct'.",
        "<b>Tool-calling instead of JSON</b>: no brittle parsing; the LLM's scale_replicas calls are the "
        "action, and the MCP layer clamps/validates at call time.",
        "<b>inspect_infrastructure as the primary tool</b>: it surfaces utilization, headroom, required "
        "replicas and budgets per slice, so the LLM defers to the model.",
        "<b>Verification gate + offline hindsight oracle</b>: gate = runtime safety; oracle = offline "
        "scoring against future load. Kept separate so the oracle never leaks into the system.",
        "<b>Baselines ordered from dumb to ideal</b>: threshold → hpa → predict-then-threshold → "
        "capacity-rule, so the LLM is judged against a ladder, not a single strawman.",
        "<b>Ollama cloud models over localhost</b>: no token, OpenAI-compatible; 3 models kept, "
        "mistral dropped.",
        "<b>numpy + stdlib core</b> (no sklearn/pandas/gym in src/); pandas/jupyter/matplotlib/reportlab "
        "only in a .venv for notebooks and PDFs.",
    ])
    S.append(Spacer(1, 8))

    # 5. Results
    S.append(Paragraph("5. Final results (per-slice closed loop)", h2))
    S.append(Paragraph("Ramp, 100 states. llm-* = tool-calling LLM (inspect_infrastructure + "
                       "scale_replicas).", body))
    S.append(Paragraph("<b>Caveat:</b> single run, no repetitions. Baselines are deterministic; "
                       "each LLM result is one trajectory per model per scenario — no error bars, "
                       "variance not measured.", body))
    b = exp["benchmark"]["ramp"]
    rows = [["method", "viol%", "repl", "under", "over", "mae"]]
    for m, met in b.items():
        rows.append([m, _fmt(met["viol%"]), _fmt(met["avg_replicas"]),
                     _fmt(met["under"]), _fmt(met["over"]), _fmt(met["mae"])])
    S.append(grid(rows, [4.4 * cm] + [1.9 * cm] * 5))
    S.append(Spacer(1, 4))
    S.append(Paragraph("steady (80 states) and spike (80 states) hold the same ordering: capacity-rule "
                       "lowest violation (~0.8–1.7%), then llm-glm5.3 / llm-flash, then hpa/threshold. "
                       "Full tables in analysis_results.pdf.", body))
    S.append(Spacer(1, 6))

    S.append(Paragraph("5.1 Research questions answered", h3))
    bl([
        "<b>RQ1 (valid, safe changes)</b>: yes within tested scenarios — gate enforces bounds, "
        "tool_trace.json confirms correct calls, rejections proven in unit tests. Claim 'measured "
        "rejection rates', never '100% safe'.",
        "<b>RQ2 (under/over vs oracle)</b>: closed-loop, flash and glm-5.3 over-provision (over "
        "0.31–0.85), deepseek under-provisions (under 0.81–1.11). The inspect tool does NOT collapse "
        "the closed-loop error the way it did in isolated A/B.",
        "<b>RQ3 (latency/cost)</b>: flash 2.8s &lt; glm-5.3 4.6s &lt; deepseek 7.2s; mistral ~2× tokens "
        "and excluded.",
        "<b>RQ4 (YAML vs MCP)</b>: both wired, not head-to-head. MCP typed tools are safer by "
        "construction (bounds at call time).",
        "<b>RQ5 (estimate_capacity)</b>: cuts MAE 1.22→0.22 and cost 3.53→2.57 but raises violation "
        "3.3%→10.0% (exact, not safer). inspect_infrastructure is the better tool.",
        "<b>RQ6 (LLM vs rules)</b>: tool-calling LLM beats threshold/hpa (5.4–16.7 vs 14.6–28.4%) but "
        "trails capacity-rule (~1%).",
    ])
    S.append(Spacer(1, 8))

    # 6. capacity-rule note (explicit)
    S.append(Paragraph("6. capacity-rule: an interesting baseline, but too expensive", h2))
    S.append(Paragraph("capacity-rule is the most interesting non-LLM baseline — it reaches ~1% "
                       "violation with a trivial deterministic rule. But it does so by <b>over-provisioning</b>: "
                       "it holds the highest mean replicas of any method (3.73–4.28 vs hpa 2.24–2.63 and "
                       "the LLM 2.62–3.50).", body))
    S.append(Paragraph("It is <b>not</b> prescient — it sees the same payload as the LLM (current load + "
                       "forecast + p_violation) and shares the oracle's required_replicas <i>formula</i>, "
                       "not its future <i>data</i>. Its edge is hysteresis: it scales up on forecast "
                       "violation but only scales down one replica at a time, so it ratchets up and stays "
                       "high, buying safety with idle capacity.", body))
    S.append(Paragraph("So it is a useful <b>upper bound</b> on safety (the ceiling the model allows), "
                       "but too expensive to be a practical controller — it wastes compute to buy low "
                       "violation. Keep it as the reference, not as a competitor to beat.", body))
    S.append(Spacer(1, 8))

    # 7. What went well
    S.append(Paragraph("7. What went well", h2))
    bl([
        "End-to-end loop closed early: dataset → env → model → oracle → gate → MCP → LLM → benchmark "
        "→ report, with 8 passing pytest tests.",
        "Tool-call-as-answer removed the whole JSON-parsing fragility; the action is read straight "
        "from the last scale_replicas call per slice.",
        "One analytic capacity model reused everywhere eliminated inconsistency and made every part "
        "comparable.",
        "inspect_infrastructure is a genuinely good tool: in isolation it drops every model's MAE to "
        "≈0 by handing the LLM the model's answer.",
        "Resumable experiment scripts meant rate-limit crashes only lost the current model, not the "
        "whole run.",
        "The 'tool, not the model, wins' finding (from isolation) is a real, honest result worth "
        "keeping in the paper — with the caveat that the closed loop is different.",
    ])
    S.append(Spacer(1, 8))

    # 8. What went wrong
    S.append(Paragraph("8. What went wrong (and the fix)", h2))
    bl([
        "<b>Constant load</b>: maxAvgLambda is fixed (18 Mbps), so aggregate load looked flat — "
        "switched to per-slice bandwidth from the slices JSON as the load signal.",
        "<b>numpy truthiness</b>: `if delays` on an array raised ValueError — changed to `if len(delays)`.",
        "<b>reportlab name collision</b>: `cm` (capacity_model alias) clashed with reportlab's `cm` "
        "unit — renamed the import to `cmod`.",
        "<b>matplotlib API change</b>: 3.11 removed `boxplot(labels=)` — changed to `tick_labels=`.",
        "<b>Notebook cwd</b>: running from notebooks/ broke the relative dataset path — added sys.path "
        "+ os.chdir bootstrap in the first cell.",
        "<b>Notebook JSONDecodeError</b>: single-round reconstruction assumed a final JSON — made the "
        "harness loop robust over rounds.",
        "<b>inspect_infrastructure string-state bug</b>: a model passed the state as a double-encoded "
        "JSON string and got zeros back — added json.loads + 'slices' unwrap.",
        "<b>429 rate limits / timeouts</b>: hit repeatedly (once lost credits mid-run) — added retry "
        "with backoff in chat(), then in _post(); added 5s spacing between decisions.",
        "<b>pkill self-match</b>: a pkill pattern matched the running shell and killed it (exit 144) — "
        "avoided patterns that match the command line.",
        "<b>PDF prompt clipping</b>: a preformatted prompt got cut off — switched to Paragraph with "
        "&lt;/&gt; escaping.",
        "<b>architecture.png stretched</b>: 4.86:1 forced to 2:1 — fixed to width=16cm, height=3.3cm.",
        "<b>env off-by-one</b>: loop ran one step too many — tests adjusted to 3 steps.",
        "<b>Resumability skipped stale data</b>: inspect_scenarios and tool_trace skipped everything "
        "because old results existed — deleted the stale JSONs and re-ran fresh.",
        "<b>_post had no retry</b>: a single 180s timeout killed the whole benchmark — added 6× retry "
        "with 60s backoff (mirroring chat()).",
        "<b>mistral-large-4</b>: ~3× slower, ~2× tokens, identical decisions — excluded as pure cost.",
    ])
    S.append(Spacer(1, 8))

    # 9. What can be better
    S.append(Paragraph("9. What can be better (future work)", h2))
    bl([
        "<b>Real cluster, not simulation</b>: run the gate against kind + Open5GS so the K8s change is "
        "applied and the KPI is measured, not recomputed.",
        "<b>Mode T vs Mode D head-to-head</b>: the plan defined both; only the combined system was "
        "tested. Separate fidelity (faithful compile) from decision quality.",
        "<b>YAML vs MCP head-to-head</b>: both are wired but never compared quantitatively.",
        "<b>Fix or drop predict-then-threshold</b>: it degenerates to hpa (the MLP over-predicts "
        "delay). Either retrain the MLP or replace the baseline.",
        "<b>Repetitions / variance</b>: only one run per model; temp 0 helps but is not bit-identical. "
        "Report N runs + std.",
        "<b>Perturb the oracle</b>: oracle and estimate_capacity share the same model (circularity). "
        "Perturb one to prove the result is not trivial.",
        "<b>Small local LLM</b>: RQ3 asked local vs commercial, but only cloud models ran. Add a "
        "3–7B local model.",
        "<b>Ablations</b>: raw numbers vs qualitative labels, with/without uncertainty, with/without "
        "current cluster state — none of these were run.",
        "<b>Closed-loop vs isolated mismatch</b>: state explicitly that the inspect tool helps in "
        "isolation but does not close the closed-loop gap, since the oracle scores future load.",
    ])
    S.append(Spacer(1, 8))

    # 10. Pointers
    S.append(Paragraph("10. Where everything lives", h2))
    bl([
        "analysis_results.pdf — final merged report.",
        "PLAN.md — plan + findings (§15).",
        "docs/findings.md — consolidated state.",
        "docs/writing-the-paper.md — paper process.",
        "results/*.json — raw data.",
        "papers/reference_matrix.md — related work.",
        "notebooks/ — EDA + LLM harness.",
    ])

    doc.build(S)
    return OUT


if __name__ == "__main__":
    print("wrote", build_pdf())

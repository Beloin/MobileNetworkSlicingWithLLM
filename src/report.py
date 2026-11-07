"""Generate initial_results.pdf from results/experiment_results.json."""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
OUT = os.path.join(REPO_ROOT, "initial_results.pdf")
MODELS = ["glm-5.3-flash:cloud", "glm-5.3:cloud",
          "mistral-large-4:cloud", "deepseek-v4-pro:cloud"]


def _fmt(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "-"
    return f"{x:.2f}"


def load():
    with open(os.path.join(RESULTS_DIR, "experiment_results.json")) as f:
        return json.load(f)


def make_graphs(res):
    bench = res["benchmark"]["ramp"]
    methods = list(bench.keys())
    viol = [bench[m]["viol%"] for m in methods]
    repl = [bench[m]["avg_replicas"] for m in methods]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    x = range(len(methods))
    a1.bar(x, viol, color="#4c72b0")
    a1.set_xticks(list(x)); a1.set_xticklabels(methods, rotation=30, ha="right")
    a1.set_ylabel("SLA violation %"); a1.set_title("Violation rate (ramp)")
    a2.bar(x, repl, color="#55a868")
    a2.set_xticks(list(x)); a2.set_xticklabels(methods, rotation=30, ha="right")
    a2.set_ylabel("mean replicas"); a2.set_title("Resource cost (ramp)")
    fig.tight_layout()
    p1 = os.path.join(RESULTS_DIR, "benchmark.png")
    fig.savefig(p1, dpi=110); plt.close(fig)

    models = [m for m in MODELS if m in res["llm"]]
    lat = [np.mean([c.get("latency_ms", 0) for c in res["llm"][m] if "latency_ms" in c])
           for m in models]
    tok = [np.mean([c.get("usage", {}).get("total_tokens", 0)
                    for c in res["llm"][m] if "usage" in c]) for m in models]
    slices = ["eMBB", "URLLC", "mMTC"]
    acts = {s: [np.mean([c["actions"][s] for c in res["llm"][m] if "actions" in c])
                for m in models] for s in slices}

    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(15, 4))
    x = np.arange(len(models))
    a1.bar(x, lat, color="#dd8452")
    a1.set_xticks(x); a1.set_xticklabels(models, rotation=15, ha="right")
    a1.set_ylabel("mean latency (ms)"); a1.set_title("LLM decision latency")
    a2.bar(x, tok, color="#c44e52")
    a2.set_xticks(x); a2.set_xticklabels(models, rotation=15, ha="right")
    a2.set_ylabel("mean total tokens"); a2.set_title("LLM token cost")
    w = 0.25
    for i, s in enumerate(slices):
        a3.bar(x + (i - 1) * w, acts[s], w, label=s)
    a3.set_xticks(x); a3.set_xticklabels(models, rotation=15, ha="right")
    a3.set_ylabel("mean replicas"); a3.set_title("Mean decision per slice")
    a3.legend(fontsize=7)
    fig.tight_layout()
    p2 = os.path.join(RESULTS_DIR, "llm.png")
    fig.savefig(p2, dpi=110); plt.close(fig)
    return p1, p2


def build_pdf(res):
    doc = SimpleDocTemplate(OUT, pagesize=A4,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)
    ss = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=18, spaceAfter=6)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=13, spaceBefore=10, spaceAfter=4)
    body = ParagraphStyle("body", parent=ss["BodyText"], fontSize=10, leading=13)

    story = [Paragraph("Initial Results: Two-Tier Control Plane for 6G Slicing", h1),
             Paragraph("Dataset: network slicing dataset (Farreras et al. 2024, Zenodo 10610616). "
                       "Prototype-first, 1-month scope.", body),
             Spacer(1, 8)]

    # 1. Pipeline
    story.append(Paragraph("1. Pipeline steps", h2))
    steps = [
        "1. Load a sample: per-slice offered load (eMBB / URLLC / mMTC) + global delay/loss.",
        "2. Tier 1 (fast ML): linear forecaster predicts next aggregate load; numpy MLP predicts delay; p_violation from delay vs budget.",
        "3. Analytic capacity model converts per-slice load -> required replicas.",
        "4. Payload = per-slice KPIs + ML signals + current replicas -> Tier 2 LLM.",
        "5. LLM proposes per-slice replica counts (MCP typed tool, or YAML manifest).",
        "6. Verification gate checks schema + policy, then applies.",
        "7. Hindsight oracle (offline, greedy P95) scores the decision vs future load.",
    ]
    for s in steps:
        story.append(Paragraph(s, body))
    story.append(Spacer(1, 8))

    # 2. Models
    story.append(Paragraph("2. Models", h2))
    story.append(Paragraph("<b>Tier 1 (fast ML):</b> linear forecaster (window 5) + numpy MLP "
                           "regressor (load -> delay), no sklearn. Baseline: predict-then-threshold.", body))
    story.append(Paragraph("<b>Tier 2 (LLM, Ollama cloud over localhost, OpenAI-compatible):</b> "
                           + ", ".join(MODELS) + ". Temperature 0, JSON output.", body))
    story.append(Paragraph("<b>Actuation:</b> MCP typed tools (estimate_capacity, scale_replicas, "
                           "set_resources, add_nf_instance, apply_k8s_manifest).", body))
    story.append(Paragraph("<b>Ground truth:</b> analytic capacity model + greedy P95 hindsight "
                           "oracle (prescient: looks at future load; offline only).", body))
    story.append(Spacer(1, 8))

    # 3. Method and controllers
    story.append(Paragraph("3. Method and controllers (detailed)", h2))
    mono = ParagraphStyle("mono", parent=ss["Code"], fontSize=8, leading=10, leftIndent=14)
    story.append(Paragraph("<b>Harness:</b> every controller — threshold, HPA, predict-then-threshold, "
        "LLM stub, real LLM — is the same decide(obs) -&gt; action function. run_method feeds each action to "
        "the env (analytic capacity model -&gt; delay/loss -&gt; violation) and to the hindsight oracle "
        "(future-load P95 -&gt; required). metrics() aggregates the outcome. Every row in the results table is "
        "measured identically; only the decision policy differs.", body))
    story.append(Paragraph("<b>Environment / capacity model:</b> per slice state = {load, replicas, delay, "
        "loss}; action = {slice: replicas}, clamped to [1,5]. effective_capacity = replicas * cap_per_replica. "
        "rho = load / capacity. delay = base_delay / (1 - rho) if rho &lt; 1 else max_delay. "
        "loss = (load - capacity) / load when overloaded, else 0. violation = delay &gt; delay_budget or "
        "loss &gt; loss_budget. One NFConfig per slice: URLLC tight delay (4x base), eMBB loose (30x base), "
        "mMTC strict loss (0.5%).", body))
    story.append(Paragraph("<b>Hindsight oracle (offline):</b> at step t, look at future per-slice load over "
        "horizon H=5 (offset d=1), take the P95, required = ceil(P95 / (cap * target_util)). Label "
        "up/down/hold vs the chosen action. Prescient — used only for scoring, never shown to the system.", body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>threshold</b> — reactive; acts only after a violation, so always one step late.", body))
    story.append(Paragraph("if delay &gt; budget: replicas = required(load)<br/>"
                           "elif delay &lt; 0.5*budget and replicas &gt; min: replicas -= 1<br/>"
                           "else: hold", mono))
    story.append(Paragraph("<b>hpa</b> — ideal controller; always matches the capacity model (mae 0). Its "
        "residual violation is the max_replicas=5 cap at peak load.", body))
    story.append(Paragraph("replicas = required(load) = ceil(load / (cap * target_util))", mono))
    story.append(Paragraph("<b>predict-then-threshold</b> — ML baseline: linear forecaster predicts next "
        "aggregate load, a numpy MLP (load -&gt; delay) predicts delay, then a threshold decides. Degenerates "
        "to HPA here because the MLP over-predicts delay, so it almost always scales up.", body))
    story.append(Paragraph("pred_delay = mlp(forecaster(history))<br/>"
                           "if pred_delay &gt; budget: scale every slice to required(load)<br/>"
                           "elif pred_delay &lt; 0.5*budget: scale down<br/>else: hold", mono))
    story.append(Paragraph("<b>llm-stub</b> — deterministic, no-network stand-in for the real LLM. Same "
        "payload in, fixed rule out. Runs the 100-step loop instantly and reproducibly. Numbers are not "
        "hand-set: the switch-case only picks the action; the env and oracle produce the metrics. It shares "
        "the same required_replicas capacity model as the oracle, so it is a near-optimal upper-bound "
        "reference — intentionally close to the solution, not a competitor to beat. It shows the ceiling "
        "the model allows.", body))
    story.append(Paragraph("if p_violation &gt; 0.5 and required &gt; current: replicas = required<br/>"
                           "elif p_violation &lt; 0.1 and current &gt; min: replicas -= 1<br/>"
                           "else: hold", mono))
    story.append(Paragraph("<b>llm-real</b> — glm-5.3-flash:cloud via Ollama (OpenAI-compatible, localhost, "
        "no token), temperature 0. Receives the per-slice payload + ML signals and outputs JSON "
        "{actions, reason}. ~6 s per decision. Conservative: over-provisions (over=0.96) to keep violation "
        "at 7.7%.", body))
    story.append(Spacer(1, 8))

    # 4. Metrics and why
    story.append(Paragraph("4. Metrics used and why", h2))
    metric_rows = [
        ["Metric", "Why it matters"],
        ["SLA violation %", "Outcome: how often delay/loss exceeds the slice budget (the cost the operator cares about)."],
        ["mean replicas", "Resource cost: over-provisioning wastes compute."],
        ["under-scaling", "Missed scale-ups (replicas below oracle requirement) - the key small-model failure."],
        ["over-scaling", "Unnecessary scale-ups (replicas above oracle requirement)."],
        ["scale-up recall / precision", "Decision quality: does the controller scale up when it should (recall) and only then (precision)."],
        ["hold correctness", "Does the controller leave well-enough alone when no change is needed."],
        ["MAE vs intended", "Fidelity: distance from the ideal capacity-model decision (Mode T)."],
        ["latency / tokens", "Tier-2 cost: wall-clock and token cost of the LLM decision (RQ3)."],
    ]
    t = Table(metric_rows, colWidths=[4.2 * cm, 12.8 * cm])
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
        ("FONT", (0, 1), (-1, -1), "Helvetica", 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # 4. Benchmark results
    story.append(Paragraph("5. Benchmark results (per-slice closed loop)", h2))
    for scen in res["benchmark"]:
        label = scen if scen != "ramp-llm" else "ramp-llm (34 states, includes real LLM)"
        story.append(Paragraph(f"Scenario: <b>{label}</b>", body))
        mm = res["benchmark"][scen]
        rows = [["method", "viol%", "repl", "under", "over", "upRec", "upPrec", "holdOk", "mae"]]
        for m, met in mm.items():
            rows.append([m, _fmt(met["viol%"]), _fmt(met["avg_replicas"]),
                         _fmt(met["under"]), _fmt(met["over"]),
                         _fmt(met["up_recall"]), _fmt(met["up_prec"]),
                         _fmt(met["hold_ok"]), _fmt(met["mae"])])
        t = Table(rows, colWidths=[3.4 * cm] + [1.55 * cm] * 8)
        t.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
            ("FONT", (0, 1), (-1, -1), "Helvetica", 8),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
        ]))
        story.append(t)
        story.append(Spacer(1, 5))
    story.append(Spacer(1, 6))

    # 6. RQ5
    if "rq5" in res:
        rq = res["rq5"]
        story.append(Paragraph("6. RQ5 — does the estimate_capacity tool help?", h2))
        story.append(Paragraph(f"Same model ({rq['model']}), same {rq['states']} states, with vs without "
            "tool-calling. Tool mode routes calls through the MCP server (estimate_capacity + scale_replicas).", body))
        rows = [["mode", "viol%", "repl", "mae", "under", "over"]]
        for mode in ["no_tool", "tool"]:
            m = rq[mode]
            rows.append([mode, _fmt(m["viol%"]), _fmt(m["avg_replicas"]),
                         _fmt(m["mae"]), _fmt(m["under"]), _fmt(m["over"])])
        t = Table(rows, colWidths=[3.4 * cm] + [2.2 * cm] * 5)
        t.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
            ("FONT", (0, 1), (-1, -1), "Helvetica", 8),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
        ]))
        story.append(t)
        story.append(Paragraph("Finding: the tool cuts MAE 1.18 -> 0.20 and cost 3.47 -> 2.55 replicas "
            "(the LLM defers to the model), but raises violation 6.7% -> 11.7% because the model's 0.7 "
            "target utilization is tighter than the LLM's own headroom. The tool makes the LLM exact, "
            "not safer.", body))
        story.append(Spacer(1, 6))

    # 7. LLM calls
    story.append(Paragraph("7. LLM calls (4 per model)", h2))
    rows = [["model", "call", "eMBB", "URLLC", "mMTC", "lat(ms)", "tokens", "reason"]]
    for m in MODELS:
        if m not in res["llm"]:
            continue
        for c in res["llm"][m]:
            if "error" in c:
                rows.append([m, str(c["call"]), "-", "-", "-", "-", "-", c["error"][:28]])
            else:
                a = c["actions"]
                rows.append([m, str(c["call"]), str(a.get("eMBB")), str(a.get("URLLC")),
                             str(a.get("mMTC")), _fmt(c.get("latency_ms")),
                             str(c.get("usage", {}).get("total_tokens", "-")),
                             (c.get("reason") or "")[:28]])
    t = Table(rows, colWidths=[3.6 * cm, 1.0 * cm, 1.2 * cm, 1.2 * cm, 1.2 * cm,
                               1.6 * cm, 1.4 * cm, 4.6 * cm])
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
        ("FONT", (0, 1), (-1, -1), "Helvetica", 7),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # 6. Graphs
    story.append(Paragraph("8. Comparison graphs", h2))
    p1, p2 = make_graphs(res)
    story.append(Image(p1, width=16 * cm, height=5.8 * cm))
    story.append(Spacer(1, 6))
    story.append(Image(p2, width=16 * cm, height=4.3 * cm))

    doc.build(story)
    return OUT


if __name__ == "__main__":
    res = load()
    out = build_pdf(res)
    print(f"wrote {out}")

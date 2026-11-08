"""Generate analysis.pdf — expanded report: dataset EDA, KPIs, tools, traces,
LLMs, and all experiments."""
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
                                TableStyle, Image, Preformatted)

from .dataset import load_result_dir, sorted_by_load, loads_by_slice
from . import capacity_model as cmod
from . import benchmark as bench
from .llm_compiler import SYSTEM_TOOL

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
OUT = os.path.join(REPO_ROOT, "analysis.pdf")
DATA = bench.DEFAULT_DIR
MODELS = ["glm-5.3-flash:cloud", "glm-5.3:cloud",
          "mistral-large-4:cloud", "deepseek-v4-pro:cloud"]
FAST_MODELS = ["glm-5.3-flash:cloud", "deepseek-v4-pro:cloud", "glm-5.3:cloud"]


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


def make_graphs(res):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    # benchmark viol + repl (ramp)
    b = res["benchmark"]["ramp"]
    methods = list(b.keys())
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    x = range(len(methods))
    a1.bar(x, [b[m]["viol%"] for m in methods], color="#4c72b0")
    a1.set_xticks(list(x)); a1.set_xticklabels(methods, rotation=35, ha="right")
    a1.set_ylabel("SLA violation %"); a1.set_title("Violation (ramp)")
    a2.bar(x, [b[m]["avg_replicas"] for m in methods], color="#55a868")
    a2.set_xticks(list(x)); a2.set_xticklabels(methods, rotation=35, ha="right")
    a2.set_ylabel("mean replicas"); a2.set_title("Cost (ramp)")
    fig.tight_layout()
    p1 = os.path.join(RESULTS_DIR, "benchmark.png"); fig.savefig(p1, dpi=110); plt.close(fig)

    # llm latency/tokens/actions (single-shot)
    models = [m for m in MODELS if m in res.get("llm", {})]
    lat = [np.mean([c.get("latency_ms", 0) for c in res["llm"][m] if "latency_ms" in c]) for m in models]
    tok = [np.mean([c.get("usage", {}).get("total_tokens", 0) for c in res["llm"][m] if "usage" in c]) for m in models]
    slices = ["eMBB", "URLLC", "mMTC"]
    acts = {s: [np.mean([c["actions"][s] for c in res["llm"][m] if "actions" in c]) for m in models] for s in slices}
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(15, 4))
    x = np.arange(len(models))
    a1.bar(x, lat, color="#dd8452"); a1.set_xticks(x); a1.set_xticklabels(models, rotation=15, ha="right")
    a1.set_ylabel("mean latency (ms)"); a1.set_title("LLM latency")
    a2.bar(x, tok, color="#c44e52"); a2.set_xticks(x); a2.set_xticklabels(models, rotation=15, ha="right")
    a2.set_ylabel("mean total tokens"); a2.set_title("Token cost")
    w = 0.25
    for i, s in enumerate(slices):
        a3.bar(x + (i - 1) * w, acts[s], w, label=s)
    a3.set_xticks(x); a3.set_xticklabels(models, rotation=15, ha="right")
    a3.set_ylabel("mean replicas"); a3.set_title("Decision per slice"); a3.legend(fontsize=7)
    fig.tight_layout()
    p2 = os.path.join(RESULTS_DIR, "llm.png"); fig.savefig(p2, dpi=110); plt.close(fig)
    return p1, p2


def build_pdf():
    states, delays, losses = load_result_dir(DATA)
    states, delays, losses = sorted_by_load(states, delays, losses)
    delays = np.asarray(delays); losses = np.asarray(losses)
    agg = np.asarray([sum(s.values()) for s in states])
    lbs = loads_by_slice(states)
    cfgs = bench.build_cfgs(states, delays)

    exp = load_json("experiment_results.json")
    inspect = load_json("inspect_test.json") if os.path.exists(os.path.join(RESULTS_DIR, "inspect_test.json")) else {}
    trace = load_json("tool_trace.json") if os.path.exists(os.path.join(RESULTS_DIR, "tool_trace.json")) else {}
    iscen = load_json("inspect_scenarios.json") if os.path.exists(os.path.join(RESULTS_DIR, "inspect_scenarios.json")) else {}

    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)
    ss = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=18, spaceAfter=6)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=13, spaceBefore=10, spaceAfter=4)
    body = ParagraphStyle("body", parent=ss["BodyText"], fontSize=9.5, leading=12.5)
    mono = ParagraphStyle("mono", parent=ss["Code"], fontSize=7.5, leading=9.5, leftIndent=8)
    cellstyle = ParagraphStyle("cell", parent=ss["BodyText"], fontSize=7.5, leading=9)

    S = [Paragraph("6G Slicing — Two-Tier Control Plane: Full Analysis", h1),
         Paragraph("Prototype report. Dataset: Farreras et al. 2024 (Zenodo 10610616). "
                   "Analytic capacity model + per-slice LLM/MCP compiler.", body),
         Spacer(1, 8)]

    # 1. Dataset EDA
    S.append(Paragraph("1. Dataset (EDA)", h2))
    S.append(Paragraph(f"{len(states)} samples. Aggregate load {agg.min():.0f}–{agg.max():.0f} Mbps "
                       f"(mean {agg.mean():.0f}).", body))
    head_rows = [["eMBB Mbps", "URLLC Mbps", "mMTC Mbps", "delay", "loss"]]
    for i in range(10):
        head_rows.append([f"{states[i]['eMBB']:.0f}", f"{states[i]['URLLC']:.0f}",
                          f"{states[i]['mMTC']:.0f}", f"{delays[i]:.5f}", f"{losses[i]:.3f}"])
    S.append(Paragraph("Head (first 10 samples):", body))
    S.append(grid(head_rows, [2.6 * cm] * 5))
    S.append(Spacer(1, 4))
    stats = [["slice", "min load", "max load", "mean load", "% of total"]]
    tot = sum(np.mean(lbs[s]) for s in cmod.SLICES)
    for s in cmod.SLICES:
        stats.append([s, f"{min(lbs[s]):.0f}", f"{max(lbs[s]):.0f}",
                      f"{np.mean(lbs[s]):.0f}", f"{100 * np.mean(lbs[s]) / tot:.0f}%"])
    S.append(Paragraph("Per-slice load:", body))
    S.append(grid(stats, [2.8 * cm, 2.6 * cm, 2.6 * cm, 2.6 * cm, 2.6 * cm]))
    S.append(Spacer(1, 4))
    S.append(Paragraph(f"KPI: delay min={delays.min():.5f} max={delays.max():.5f} mean={delays.mean():.5f} "
                       f"| loss min={losses.min():.3f} max={losses.max():.3f} mean={losses.mean():.3f}", body))
    S.append(Spacer(1, 8))

    # 2. Model + KPIs
    S.append(Paragraph("2. Tier-1 components + KPI budgets", h2))
    bullet = ParagraphStyle("bullet2", parent=body, leftIndent=14, bulletIndent=2, spaceAfter=1)
    S.append(Paragraph("• <b>Capacity model</b> — analytic, deterministic (not ML); the scaling math every other part trusts:", bullet))
    S.append(Preformatted(
        "effective_capacity = replicas * cap_per_replica\n"
        "rho = load / capacity\n"
        "delay = base_delay / (1 - rho)  if rho < 1 else max_delay\n"
        "loss  = (load - capacity) / load if overloaded else 0\n"
        "violation = delay > delay_budget OR loss > loss_budget\n"
        "required_replicas = ceil(load / (cap * target_util))", mono))
    S.append(Paragraph("• calibrated from the slice's P95 load (cap) and the dataset's min delay (base_delay); feeds the env, oracle, gate, baselines and MCP tools.", bullet))
    S.append(Paragraph("• <b>Forecaster</b> — learned. Predicts next aggregate load: linear regression over the last 5 points (or persistence). Output: forecast_mbps.", bullet))
    S.append(Paragraph("• <b>KPI predictor</b> — learned. Numpy MLP regressor (16 hidden, ReLU, MSE) trained on aggregate load → delay. p_violation = sigmoid((pred_delay − budget)/budget).", bullet))
    S.append(Spacer(1, 4))
    kpi = [["slice", "cap/replica Mbps", "delay_budget (x base)", "loss_budget"]]
    for s in cmod.SLICES:
        c = cfgs[s]
        kpi.append([s, f"{c.cap_per_replica_mbps:.0f}",
                    f"{c.delay_budget / c.base_delay:.0f}x", f"{c.loss_budget}"])
    S.append(grid(kpi, [2.8 * cm, 3.6 * cm, 4.2 * cm, 2.6 * cm]))
    S.append(Spacer(1, 8))

    # 3. Pipeline + harness
    S.append(Paragraph("3. Pipeline + harness", h2))
    for line in [
        "dataset sample -> per-slice load -> Tier1 (forecaster + MLP) -> payload -> LLM (or stub) -> gate -> apply",
        "hindsight oracle (offline): future-load P95 -> required replicas, scores under/over-scaling",
        "every controller is decide(obs) -> action; run_method feeds it to env + oracle; metrics() aggregates",
    ]:
        S.append(Paragraph("• " + line, body))
    S.append(Image(os.path.join(REPO_ROOT, "docs", "architecture.png"), width=16 * cm, height=3.3 * cm))
    S.append(Image(os.path.join(REPO_ROOT, "docs", "harness.png"), width=13 * cm, height=7.5 * cm))
    S.append(Spacer(1, 8))

    # 4. Methods
    S.append(Paragraph("4. Methods", h2))
    S.append(Paragraph("<b>threshold</b> — reactive: scale only after violation. <b>hpa</b> — ideal "
        "controller, always required_replicas(load). <b>predict-then-threshold</b> — MLP delay prediction "
        "then threshold (degenerates to HPA). <b>llm-stub</b> — deterministic rule, near-optimal reference. "
        "<b>llm-real</b> — Ollama cloud LLM, JSON or tool-calling.", body))
    S.append(Spacer(1, 8))

    # 5. LLM + prompt + tools
    S.append(Paragraph("5. LLMs, prompt, tools", h2))
    S.append(Paragraph("Models (Ollama cloud, localhost, OpenAI-compatible, temp 0): "
                       + ", ".join(MODELS), body))
    S.append(Paragraph("<b>Note:</b> mistral-large-4 is excluded from the tool and scenario experiments — "
                       "~3x slower and ~2x more tokens than the others while returning the same decisions.", body))
    S.append(Paragraph("System prompt (tool mode):", body))
    S.append(Preformatted(SYSTEM_TOOL, mono))
    S.append(Spacer(1, 4))
    tools = [
        ["tool", "does"],
        ["estimate_capacity(slice, load)", "load -> required replicas (capacity model)"],
        ["scale_replicas(slice, n)", "validate + clamp n to [1,5]"],
        ["set_resources(slice, cpu, mem)", "resource-limit manifest patch"],
        ["add_nf_instance(slice, region)", "register a new NF instance"],
        ["apply_k8s_manifest(id, yaml)", "validate a Deployment manifest"],
        ["inspect_infrastructure(state)", "utilization, capacity, headroom, required, budgets per slice"],
    ]
    S.append(grid(tools, [6.5 * cm, 9.5 * cm]))
    S.append(Spacer(1, 8))

    # 6. Function-call traces
    if trace:
        S.append(Paragraph("6. Function-call traces (sample)", h2))
        for model, rows in trace.items():
            if not rows:
                continue
            r0 = rows[0]
            S.append(Paragraph(f"<b>{model}</b> (state i={r0['i']}) — final actions {r0['actions']}", body))
            tr = [["tool call", "arguments", "result"]]
            for tc in r0["trace"]:
                name = tc["name"]
                res = tc["result"]
                if name == "inspect_infrastructure":
                    args_s = "state (3 slices)"
                    inf = res.get("infra", {})
                    summary = "  ".join(f"{s}: util={inf[s]['utilization']} req={inf[s]['required_replicas']}"
                                       for s in cmod.SLICES)
                elif name == "scale_replicas":
                    a = tc["args"]
                    args_s = f"{a.get('slice_type')} -> {a.get('replicas')}"
                    summary = "ok" if res.get("ok") else f"error: {res.get('reason')}"
                else:
                    args_s = json.dumps(tc["args"])[:40]
                    summary = json.dumps(res)[:40]
                tr.append([name, args_s, Paragraph(summary, cellstyle)])
            S.append(grid(tr, [4.5 * cm, 3.5 * cm, 9.0 * cm]))
            S.append(Spacer(1, 4))
        S.append(Spacer(1, 6))

    # 7. Benchmark results
    S.append(Paragraph("7. Benchmark (per-slice closed loop)", h2))
    for scen in exp["benchmark"]:
        S.append(Paragraph(f"Scenario: <b>{scen}</b>", body))
        rows = [["method", "viol%", "repl", "under", "over", "mae"]]
        for m, met in exp["benchmark"][scen].items():
            rows.append([m, _fmt(met["viol%"]), _fmt(met["avg_replicas"]),
                         _fmt(met["under"]), _fmt(met["over"]), _fmt(met["mae"])])
        S.append(grid(rows, [3.6 * cm] + [2.0 * cm] * 5))
        S.append(Spacer(1, 4))
    S.append(Spacer(1, 6))

    # 8. RQ5
    if "rq5" in exp:
        rq = exp["rq5"]
        S.append(Paragraph("8. RQ5 — estimate_capacity tool", h2))
        rows = [["mode", "viol%", "repl", "mae", "under", "over"]]
        for mode in ["no_tool", "tool"]:
            m = rq[mode]
            rows.append([mode, _fmt(m["viol%"]), _fmt(m["avg_replicas"]),
                         _fmt(m["mae"]), _fmt(m["under"]), _fmt(m["over"])])
        S.append(grid(rows, [3.0 * cm] + [2.4 * cm] * 5))
        S.append(Paragraph("Finding: tool cuts MAE 1.18->0.20 and cost 3.47->2.55, but raises violation "
                           "6.7%->11.7% (exact, not safer).", body))
        S.append(Spacer(1, 8))

    # 9. Inspect A/B across scenarios
    if iscen:
        S.append(Paragraph("9. Inspect tool A/B — per scenario (mistral excluded)", h2))
        for scen in ["ramp", "steady", "spike"]:
            S.append(Paragraph(f"Scenario: <b>{scen}</b> (over/under/mae vs required_replicas)", body))
            rows = [["model", "arm", "over", "under", "mae"]]
            for model in FAST_MODELS:
                for arm in ["no-tool", "inspect"]:
                    key = f"{scen}|{model}|{arm}"
                    recs = iscen.get(key, [])
                    if not recs:
                        continue
                    over = float(np.mean([r["over"] for r in recs]))
                    under = float(np.mean([r["under"] for r in recs]))
                    mae = float(np.mean([r["mae"] for r in recs]))
                    rows.append([model, arm, _fmt(over), _fmt(under), _fmt(mae)])
            S.append(grid(rows, [5.2 * cm, 2.0 * cm, 1.8 * cm, 1.8 * cm, 1.8 * cm]))
            S.append(Spacer(1, 4))
        S.append(Paragraph("Finding: the tool makes capable models near-exact (deepseek and glm drop MAE "
                           "sharply) but flash regresses. Direction holds across ramp, steady and spike.", body))
        S.append(Spacer(1, 8))

    # 10. Graphs
    S.append(Paragraph("10. Comparison graphs", h2))
    p1, p2 = make_graphs(exp)
    S.append(Image(p1, width=16 * cm, height=5.8 * cm))
    S.append(Spacer(1, 6))
    S.append(Image(p2, width=16 * cm, height=4.3 * cm))

    doc.build(S)
    return OUT


if __name__ == "__main__":
    print("wrote", build_pdf())

"""Generate notebooks/eda.ipynb."""
import json
import os

cells = []


def md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "id": f"md-{len(cells)}",
                  "source": text.splitlines(True)})


def code(text):
    cells.append({"cell_type": "code", "metadata": {}, "id": f"code-{len(cells)}",
                  "execution_count": None, "outputs": [], "source": text.splitlines(True)})


md("""# EDA — Network Slicing Dataset + Pipeline Walkthrough

Dataset: Farreras et al. 2024 (Zenodo 10610616), untarred result dir
`results_slicing_WFQ_1000_routing_7800_7899` (100 samples).

This notebook does three things:
1. **EDA** — what the load and KPI distributions look like.
2. **Model** — how we turn per-slice load into replicas/delay/loss (capacity model) and how slices map to budgets.
3. **Manual test** — one sample walked through the full pipeline (Tier-1 signals -> payload -> decision -> gate -> outcome -> oracle).
""")

code("""%matplotlib inline
import sys, os
for _p in (os.getcwd(), os.path.dirname(os.getcwd())):
    if os.path.exists(os.path.join(_p, "src")):
        sys.path.insert(0, _p)
        os.chdir(_p)
        break

import json
import numpy as np
import matplotlib.pyplot as plt

from src import capacity_model as cm
from src import benchmark as bench
from src.dataset import load_result_dir, sorted_by_load, loads_by_slice
from src.kpi_predictor import MLPRegressor, violation_prob
from src.forecaster import LinearForecaster
from src.llm_compiler import build_payload, call_stub
from src import gate
from src.oracle import oracle_slices

DATA = "datasets/generation_netwok_slicing_dataset/2.2.1-10kprocessed/results_slicing_WFQ_1000_routing_7800_7899"
""")

code("""states, delays, losses = load_result_dir(DATA)
states, delays, losses = sorted_by_load(states, delays, losses)
delays = np.asarray(delays); losses = np.asarray(losses)
agg = np.asarray([sum(s.values()) for s in states])
lbs = loads_by_slice(states)

print(f"samples = {len(states)}")
print(f"aggregate load (Mbps): min={agg.min():.0f}  max={agg.max():.0f}  mean={agg.mean():.0f}")
print("one state (per-slice load, Mbps):", {s: round(states[0][s]) for s in cm.SLICES})
""")

code("""import pandas as pd

df = pd.DataFrame({
    "eMBB_load_mbps": [s["eMBB"] for s in states],
    "URLLC_load_mbps": [s["URLLC"] for s in states],
    "mMTC_load_mbps": [s["mMTC"] for s in states],
    "delay": delays,
    "loss": losses,
})
df.head(10)
""")

md("""## 1. Load distribution

Each sample is a per-slice offered load dict `{eMBB, URLLC, mMTC}` (Mbps).
`maxAvgLambda` is constant, so the per-slice bandwidth is the load signal.""")
code("""fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))
ax[0].hist(agg, bins=20)
ax[0].set_xlabel("aggregate load (Mbps)"); ax[0].set_title("aggregate load")
ax[1].boxplot([lbs[s] for s in cm.SLICES], tick_labels=cm.SLICES)
ax[1].set_ylabel("load (Mbps)"); ax[1].set_title("per-slice load")
plt.tight_layout(); plt.show()

for s in cm.SLICES:
    print(f"{s}: min={min(lbs[s]):.0f}  max={max(lbs[s]):.0f}  mean={np.mean(lbs[s]):.0f}")
""")

md("""## 2. KPI (delay / loss)

The dataset also records global delay and loss rate per sample. We use these
only to calibrate `base_delay` and train the MLP; the control loop re-derives
KPI from the capacity model.""")
code("""fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))
ax[0].scatter(agg, delays, s=6)
ax[0].set_xlabel("aggregate load (Mbps)"); ax[0].set_ylabel("global delay")
ax[0].set_title("load vs delay")
ax[1].hist(losses, bins=20)
ax[1].set_xlabel("loss rate"); ax[1].set_title("loss rate")
plt.tight_layout(); plt.show()

print(f"delay: min={delays.min():.5f}  max={delays.max():.5f}")
print(f"loss : min={losses.min():.3f}  max={losses.max():.3f}")
""")

md("""## 3. Slice composition and budgets

How we *use* the slices: each slice type gets its own `NFConfig` — a
per-replica capacity and KPI budget. URLLC = tight delay, eMBB = loose delay +
high throughput, mMTC = strict loss.""")
code("""mean_load = {s: np.mean(lbs[s]) for s in cm.SLICES}
total = sum(mean_load.values())
for s in cm.SLICES:
    print(f"{s}: mean load {mean_load[s]:.0f} Mbps ({100*mean_load[s]/total:.0f}% of total)")

base = delays.min()
caps = {s: max(np.percentile(lbs[s], 95) / (5 * 0.7), 1.0) for s in cm.SLICES}
cfgs = cm.build_slice_configs(caps, base)
for s in cm.SLICES:
    c = cfgs[s]
    print(f"{s}: cap/replica={c.cap_per_replica_mbps:.0f} Mbps, "
          f"delay_budget={c.delay_budget/c.base_delay:.0f}x base, loss_budget={c.loss_budget}")
""")

md("""## 4. Capacity model (how we model)

```
effective_capacity = replicas * cap_per_replica
rho = load / capacity
delay = base_delay / (1 - rho)  if rho < 1, else max_delay
loss  = (load - capacity) / load if overloaded, else 0
violation = delay > delay_budget OR loss > loss_budget
```
`required_replicas = ceil(load / (cap_per_replica * target_util))` keeps
utilization at the 0.7 target.""")
code("""nf = cm.NFConfig(cap_per_replica_mbps=57, base_delay=0.0002, delay_budget=0.0008, max_delay=0.002)
loads = np.linspace(10, 400, 200)
for r in [1, 3, 5]:
    d = [cm.delay(L, r, nf) for L in loads]
    plt.plot(loads, d, label=f"{r} replicas")
plt.axhline(nf.delay_budget, color="r", ls="--", label="budget")
plt.xlabel("load (Mbps)"); plt.ylabel("delay"); plt.legend()
plt.title("delay vs load, per replica count")
plt.show()
""")

md("""## 5. Manual pipeline test (one sample)

Walk sample `i=40` through the full loop: observe -> Tier-1 signals ->
payload -> stub decision -> gate -> resulting KPI -> oracle.""")
code("""cfgs = bench.build_cfgs(states, delays)
agg_nf = bench.build_agg_nf(states, delays)
pred = MLPRegressor().fit(agg, delays)
fc = LinearForecaster(window=5)

i = 40
state = states[i]
print(f"step t={i}, per-slice load (Mbps):", {s: round(state[s]) for s in cm.SLICES})

# 1. observation at min replicas (current KPI from the capacity model)
obs = {"t": i, "slices": {s: {
    "load": state[s], "replicas": cfgs[s].min_replicas,
    "delay": cm.delay(state[s], cfgs[s].min_replicas, cfgs[s]),
    "loss": cm.loss(state[s], cfgs[s].min_replicas, cfgs[s]),
} for s in cm.SLICES}}
print("obs (min replicas):",
      {s: (round(obs["slices"][s]["delay"], 5), round(obs["slices"][s]["loss"], 3)) for s in cm.SLICES})

# 2. Tier-1 signals: forecast + MLP -> p_violation
history = list(agg[:i + 1])
forecast = fc.predict(history)
pv = violation_prob(float(pred.predict([forecast])[0]), agg_nf.delay_budget)
print(f"forecast={forecast:.0f} Mbps, p_violation={pv:.2f}")

# 3. payload to the LLM
payload = build_payload(obs, forecast, pv, cfgs)
print(json.dumps(payload, indent=2)[:500], "...")

# 4. decision (stub = deterministic rule)
action = call_stub(payload, cfgs)["actions"]
print("stub action:", action)

# 5. verification gate
ok, reason = gate.check_slices(action, cfgs)
print("gate:", ok, reason)

# 6. resulting KPI at the chosen replicas
for s in cm.SLICES:
    d = cm.delay(state[s], action[s], cfgs[s])
    l = cm.loss(state[s], action[s], cfgs[s])
    v = cm.violation(d, l, cfgs[s])
    print(f"{s}: action={action[s]} -> delay={d:.5f} loss={l:.3f} violation={v}")

# 7. hindsight oracle: what was actually needed (future P95)
o = oracle_slices(lbs, i, action, cfgs)
for s in cm.SLICES:
    req, label, delta = o[s]
    print(f"{s}: oracle required={req} label={label} delta={delta}")
""")

nb = {
    "nbformat": 4, "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.14"},
    },
    "cells": cells,
}

os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notebooks"), exist_ok=True)
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notebooks", "eda.ipynb")
with open(out, "w") as f:
    json.dump(nb, f, indent=1)
print("wrote", out)

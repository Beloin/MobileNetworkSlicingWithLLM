"""Greedy P95 hindsight oracle, per slice (offline, never seen by the system).

At window t, take the future per-slice load over horizon H (offset d), P95,
compute required replicas via the capacity model, label up/down/hold vs the
chosen replicas. See PLAN.md 8.2.
"""
import numpy as np
from .capacity_model import SLICES, required_replicas


def oracle_slices(loads_by_slice, t, chosen, cfgs, horizon=5, d=1):
    out = {}
    for s in SLICES:
        fut = loads_by_slice[s][t + d: t + d + horizon]
        if not fut:
            out[s] = (chosen.get(s, cfgs[s].min_replicas), "hold", 0)
            continue
        p95 = float(np.percentile(fut, 95))
        req = required_replicas(p95, cfgs[s])
        cur = chosen.get(s, cfgs[s].min_replicas)
        label = "up" if req > cur else "down" if req < cur else "hold"
        out[s] = (req, label, req - cur)
    return out


def oracle_aggregate(loads, t, chosen, nf, horizon=5, d=1):
    """Single-resource oracle (kept for the aggregate/ML baseline path)."""
    fut = loads[t + d: t + d + horizon]
    if not fut:
        return chosen, "hold", 0
    p95 = float(np.percentile(fut, 95))
    req = required_replicas(p95, nf)
    label = "up" if req > chosen else "down" if req < chosen else "hold"
    return req, label, req - chosen

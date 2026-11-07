"""Analytic capacity model: load -> replicas / delay / loss.

Deterministic, shared by the env, oracle, gate, and every baseline. One
`NFConfig` per slice type. Delay = base_delay / (1 - rho); overloaded (rho>=1)
-> max_delay and proportional loss. Documented placeholder, not calibrated
queueing. See PLAN.md 8.1.
"""
import math
from dataclasses import dataclass

SLICES = ["eMBB", "URLLC", "mMTC"]


@dataclass
class NFConfig:
    cap_per_replica_mbps: float = 15.0
    target_util: float = 0.7
    min_replicas: int = 1
    max_replicas: int = 5
    base_delay: float = 0.001
    max_delay: float = 0.05
    delay_budget: float = 0.01
    loss_budget: float = 0.02


def effective_capacity(replicas: int, nf: NFConfig) -> float:
    return replicas * nf.cap_per_replica_mbps


def required_replicas(load: float, nf: NFConfig) -> int:
    req = math.ceil(load / (nf.cap_per_replica_mbps * nf.target_util))
    return max(nf.min_replicas, min(nf.max_replicas, req))


def delay(load: float, replicas: int, nf: NFConfig) -> float:
    c = effective_capacity(replicas, nf)
    rho = load / c if c > 0 else 1.0
    if rho >= 1.0:
        return nf.max_delay
    return nf.base_delay / (1.0 - rho)


def loss(load: float, replicas: int, nf: NFConfig) -> float:
    c = effective_capacity(replicas, nf)
    if load <= c:
        return 0.0
    return (load - c) / load


def violation(delay_: float, loss_: float, nf: NFConfig) -> bool:
    return delay_ > nf.delay_budget or loss_ > nf.loss_budget


def build_slice_configs(caps, base_delay):
    """One NFConfig per slice. caps: {slice: cap_per_replica_mbps}.

    URLLC = tight delay, eMBB = loose delay + high throughput, mMTC = strict
    loss. Calibrate caps from per-slice P95 load in the caller.
    """
    cfgs = {}
    for s in SLICES:
        c = caps.get(s, 15.0)
        if s == "URLLC":
            cfgs[s] = NFConfig(cap_per_replica_mbps=c, base_delay=base_delay,
                               max_delay=base_delay * 10.0, delay_budget=base_delay * 4.0,
                               loss_budget=0.005)
        elif s == "eMBB":
            cfgs[s] = NFConfig(cap_per_replica_mbps=c, base_delay=base_delay,
                               max_delay=base_delay * 50.0, delay_budget=base_delay * 30.0,
                               loss_budget=0.02)
        else:  # mMTC
            cfgs[s] = NFConfig(cap_per_replica_mbps=c, base_delay=base_delay,
                               max_delay=base_delay * 20.0, delay_budget=base_delay * 15.0,
                               loss_budget=0.005)
    return cfgs

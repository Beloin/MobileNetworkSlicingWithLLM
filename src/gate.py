"""Verification gate: schema + policy checks on proposed changes.

`check` validates one typed action (MCP path). `check_slices` validates a
per-slice action dict. `check_manifest` parses/validates a YAML manifest.
`decide_with_gate` wraps the gate with one retry and a hold fallback.
"""
from .capacity_model import NFConfig, SLICES
from . import manifest


def check(proposal, obs, nf: NFConfig):
    action = proposal if isinstance(proposal, (int, float)) else proposal.get("action")
    if action is None:
        return False, "schema: missing action"
    try:
        action = int(round(float(action)))
    except (TypeError, ValueError):
        return False, "schema: action not numeric"
    if not (nf.min_replicas <= action <= nf.max_replicas):
        return False, f"policy: replicas {action} outside [{nf.min_replicas},{nf.max_replicas}]"
    if action < 1:
        return False, "policy: zero replicas (destructive)"
    return True, "ok"


def check_slices(action, cfgs):
    for s in SLICES:
        if s not in action:
            return False, f"schema: missing slice {s}"
        ok, reason = check(action[s], {}, cfgs[s])
        if not ok:
            return False, f"{s}: {reason}"
    return True, "ok"


def check_manifest(text, obs, nf: NFConfig):
    try:
        kind, replicas = manifest.parse(text)
    except (ValueError, TypeError) as e:
        return False, f"schema: {e}"
    if kind != manifest.KIND:
        return False, f"policy: kind {kind} not allowed"
    return check(replicas, obs, nf)


def decide_with_gate(propose_fn, obs, nf: NFConfig, retries: int = 1):
    rejected = 0
    for _ in range(retries + 1):
        prop = propose_fn()
        ok, _ = check(prop, obs, nf)
        if ok:
            return {"action": prop["action"], "rejected": rejected}
        rejected += 1
    return {"action": obs["replicas"], "rejected": rejected}

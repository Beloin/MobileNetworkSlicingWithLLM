"""Tiny, dependency-free YAML emit/parse for the K8s change path.

Represents a Deployment replica patch as a dict and (de)serializes a YAML-like
string. Only the `replicas` field matters for Mode T fidelity. No pyyaml.
"""

KIND = "Deployment"


def emit(patch: dict) -> str:
    r = patch["spec"]["replicas"]
    return (
        "apiVersion: apps/v1\n"
        f"kind: {patch['kind']}\n"
        "metadata:\n"
        f"  name: {patch['metadata']['name']}\n"
        "spec:\n"
        f"  replicas: {r}\n"
    )


def parse(text: str):
    """Return (kind, replicas). Raise ValueError on malformed input."""
    kind = None
    replicas = None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("kind:"):
            kind = s.split(":", 1)[1].strip()
        elif s.startswith("replicas:"):
            replicas = int(s.split(":", 1)[1].strip())
    if kind is None or replicas is None:
        raise ValueError("manifest missing kind or replicas")
    return kind, replicas

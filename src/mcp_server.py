"""MCP server exposing typed tools for the K8s actuation layer.

Minimal JSON-RPC 2.0 over stdio (newline-delimited), no external deps.
Tools (PLAN.md 6.5): estimate_capacity, scale_replicas, set_resources,
add_nf_instance, apply_k8s_manifest. Each validates inputs and enforces
deterministic limits. Run as `python -m src.mcp_server` to serve over stdio.
"""
import json
import sys

from .capacity_model import SLICES, required_replicas
from .gate import check, check_manifest


def tool_schemas():
    return [
        {"name": "estimate_capacity",
         "description": "Convert a slice load (Mbps) into a required replica count.",
         "inputSchema": {"type": "object",
                         "properties": {"slice_type": {"type": "string"},
                                        "load_mbps": {"type": "number"}},
                         "required": ["slice_type", "load_mbps"]}},
        {"name": "scale_replicas",
         "description": "Propose a validated replica count for a slice (enforces bounds).",
         "inputSchema": {"type": "object",
                         "properties": {"slice_type": {"type": "string"},
                                        "replicas": {"type": "integer"}},
                         "required": ["slice_type", "replicas"]}},
        {"name": "set_resources",
         "description": "Return a resource manifest patch (CPU/mem) for a slice NF.",
         "inputSchema": {"type": "object",
                         "properties": {"slice_type": {"type": "string"},
                                        "cpu": {"type": "string"}, "mem": {"type": "string"}},
                         "required": ["slice_type", "cpu", "mem"]}},
        {"name": "add_nf_instance",
         "description": "Register a new NF instance for a slice (validated).",
         "inputSchema": {"type": "object",
                         "properties": {"slice_type": {"type": "string"},
                                        "region": {"type": "string"}},
                         "required": ["slice_type", "region"]}},
        {"name": "apply_k8s_manifest",
         "description": "Validate a K8s Deployment manifest against the gate.",
         "inputSchema": {"type": "object",
                         "properties": {"slice_id": {"type": "string"},
                                        "manifest_text": {"type": "string"}},
                         "required": ["slice_id", "manifest_text"]}},
    ]


def openai_tools(names=None):
    """Convert MCP tool schemas to OpenAI function-calling format."""
    out = []
    for t in tool_schemas():
        if names is not None and t["name"] not in names:
            continue
        out.append({"type": "function", "function": {
            "name": t["name"], "description": t["description"],
            "parameters": t["inputSchema"]}})
    return out


def estimate_capacity(slice_type, load_mbps, cfgs):
    return required_replicas(float(load_mbps), cfgs[slice_type])


def scale_replicas(slice_type, replicas, cfgs):
    ok, reason = check(replicas, {}, cfgs[slice_type])
    if not ok:
        return {"ok": False, "reason": reason}
    return {"ok": True, "slice_type": slice_type, "replicas": int(round(replicas))}


def set_resources(slice_type, cpu, mem, cfgs):
    return {"ok": True, "patch": {
        "apiVersion": "apps/v1", "kind": "Deployment",
        "metadata": {"name": f"nf-{slice_type.lower()}"},
        "spec": {"resources": {"limits": {"cpu": cpu, "memory": mem}}}}}


def add_nf_instance(slice_type, region, cfgs):
    if slice_type not in SLICES:
        return {"ok": False, "reason": f"unknown slice {slice_type}"}
    return {"ok": True, "slice_type": slice_type, "region": region, "action": "create"}


def apply_k8s_manifest(slice_id, manifest_text, cfgs):
    nf = next(iter(cfgs.values()))
    ok, reason = check_manifest(manifest_text, {"replicas": 1}, nf)
    return {"ok": ok, "reason": reason, "slice_id": slice_id}


def call_tool(name, args, cfgs):
    if name == "estimate_capacity":
        return estimate_capacity(args["slice_type"], args["load_mbps"], cfgs)
    if name == "scale_replicas":
        return scale_replicas(args["slice_type"], args["replicas"], cfgs)
    if name == "set_resources":
        return set_resources(args["slice_type"], args["cpu"], args["mem"], cfgs)
    if name == "add_nf_instance":
        return add_nf_instance(args["slice_type"], args["region"], cfgs)
    if name == "apply_k8s_manifest":
        return apply_k8s_manifest(args["slice_id"], args["manifest_text"], cfgs)
    raise ValueError(f"unknown tool {name}")


def serve(cfgs):
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = msg.get("method")
        mid = msg.get("id")
        if method == "initialize":
            resp = {"jsonrpc": "2.0", "id": mid, "result": {
                "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                "serverInfo": {"name": "slicing-mcp", "version": "0.1.0"}}}
        elif method == "notifications/initialized":
            continue
        elif method == "tools/list":
            resp = {"jsonrpc": "2.0", "id": mid, "result": {"tools": tool_schemas()}}
        elif method == "tools/call":
            p = msg.get("params", {})
            name, args = p.get("name"), p.get("arguments", {})
            try:
                r = call_tool(name, args, cfgs)
                resp = {"jsonrpc": "2.0", "id": mid, "result": {
                    "content": [{"type": "text", "text": json.dumps(r)}], "isError": False}}
            except Exception as e:
                resp = {"jsonrpc": "2.0", "id": mid, "result": {
                    "content": [{"type": "text", "text": str(e)}], "isError": True}}
        else:
            resp = {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32601, "message": "method not found"}}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    # Serve with default configs; calibration is injected by the caller in tests.
    from .capacity_model import build_slice_configs
    serve(build_slice_configs({"eMBB": 50.0, "URLLC": 30.0, "mMTC": 10.0}, 0.001))

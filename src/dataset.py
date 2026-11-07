"""Read the untarred slicing dataset into per-slice load traces.

Each sample yields per-slice aggregate offered bandwidth (Mbps), summed over
every slice's flows by slice type, plus global delay and loss rate.
`maxAvgLambda` is constant, so per-slice bandwidth is the load signal.
"""
import json
import os

from .capacity_model import SLICES


def load_result_dir(path: str):
    """Return (states, delays, losses).

    states: list of dict {slice_type: load_mbps} for the three slice types.
    """
    results = os.path.join(path, "simulationResults.txt")
    inputs = os.path.join(path, "input_files.txt")
    slices_dir = os.path.join(os.path.dirname(path), "slices")

    states, delays, losses = [], [], []
    with open(results, "r", encoding="utf-8") as fr, \
         open(inputs, "r", encoding="utf-8") as fi:
        for rline, iline in zip(fr, fi):
            rline, iline = rline.strip(), iline.strip()
            if not rline or not iline:
                continue
            packets, lost, delay = rline.split("|", 1)[0].split(",")[:3]
            packets, lost, delay = float(packets), float(lost), float(delay)
            slice_file = iline.split(";")[3]
            with open(os.path.join(slices_dir, slice_file), "r", encoding="utf-8") as fs:
                data = json.load(fs)
            loads = {s: 0.0 for s in SLICES}
            for sl in data:
                typ = sl.get("type")
                if typ in loads:
                    loads[typ] += sum(f["bandwidth"] for f in sl.get("flows", [])) / 1e6
            states.append(loads)
            delays.append(delay)
            losses.append(lost / packets if packets else 0.0)
    return states, delays, losses


def aggregate(states):
    return [sum(s.values()) for s in states]


def loads_by_slice(states):
    return {s: [st[s] for st in states] for s in SLICES}


def sorted_by_load(states, delays, losses):
    triples = sorted(zip(states, delays, losses), key=lambda t: sum(t[0].values()))
    return [t[0] for t in triples], [t[1] for t in triples], [t[2] for t in triples]

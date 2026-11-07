"""Per-slice closed-loop runner + metrics. See experiment.py for the driver."""
import os
import numpy as np

from . import capacity_model as cm
from .dataset import loads_by_slice
from .telemetry_env import SlicingEnv
from .forecaster import LinearForecaster
from .kpi_predictor import MLPRegressor, violation_prob
from .oracle import oracle_slices
from .baselines import ThresholdStateMachine, HPA, PredictThenThreshold
from .llm_compiler import build_payload, call_llm


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DIR = os.path.join(
    REPO_ROOT, "datasets", "generation_netwok_slicing_dataset",
    "2.2.1-10kprocessed", "results_slicing_WFQ_1000_routing_7800_7899")


def build_cfgs(states, delays):
    base = float(np.min(delays)) if delays else 0.001
    lbs = loads_by_slice(states)
    caps = {}
    for s in cm.SLICES:
        p95 = float(np.percentile(lbs[s], 95)) if lbs[s] else 1.0
        caps[s] = max(p95 / (5 * 0.7), 1.0)
    return cm.build_slice_configs(caps, base)


def build_agg_nf(states, delays):
    base = float(np.min(delays)) if delays else 0.001
    agg = [sum(st.values()) for st in states]
    p95 = float(np.percentile(agg, 95)) if agg else 1.0
    return cm.NFConfig(cap_per_replica_mbps=p95 / (5 * 0.7), base_delay=base,
                       max_delay=base * 20.0, delay_budget=base * 8.0,
                       loss_budget=0.02)


def run_method(states, cfgs, decide, oracle_cfgs=None):
    env = SlicingEnv(states, cfgs)
    obs = env.reset()
    hist = []
    lbs = loads_by_slice(states)
    oc = oracle_cfgs or cfgs
    out = {s: {"current": [], "action": [], "intended": [], "req": [],
               "label": [], "violation": []} for s in cm.SLICES}
    for _ in range(len(states)):
        hist.append(sum(obs["slices"][s]["load"] for s in cm.SLICES))
        d = decide(obs, hist)
        for s in cm.SLICES:
            cur = obs["slices"][s]["replicas"]
            out[s]["current"].append(cur)
            out[s]["action"].append(d.get(s, cur))
            out[s]["intended"].append(cm.required_replicas(obs["slices"][s]["load"], cfgs[s]))
        chosen = {s: d.get(s, obs["slices"][s]["replicas"]) for s in cm.SLICES}
        o = oracle_slices(lbs, obs["t"], chosen, oc)
        for s in cm.SLICES:
            out[s]["req"].append(o[s][0])
            out[s]["label"].append(o[s][1])
        obs, reward, done, info = env.step(d)
        for s in cm.SLICES:
            out[s]["violation"].append(info["slices"][s]["violation"])
        if done:
            break
    return out


def metrics(out):
    cur, act, req, lab, viol = [], [], [], [], []
    for s in cm.SLICES:
        cur += out[s]["current"]
        act += out[s]["action"]
        req += out[s]["req"]
        lab += out[s]["label"]
        viol += out[s]["violation"]
    cur = np.asarray(cur, float)
    act = np.asarray(act, float)
    req = np.asarray(req, float)
    lab = np.asarray(lab)
    viol = np.asarray(viol, float)
    up = lab == "up"
    hold = lab == "hold"
    scaled_up = act > cur
    intended = np.asarray([v for s in cm.SLICES for v in out[s]["intended"]], float)
    return {
        "viol%": 100.0 * float(viol.mean()),
        "avg_replicas": float(act.mean()),
        "under": float(np.maximum(0, req - act).mean()),
        "over": float(np.maximum(0, act - req).mean()),
        "up_recall": float(scaled_up[up].mean()) if up.any() else float("nan"),
        "up_prec": float(up[scaled_up].mean()) if scaled_up.any() else float("nan"),
        "hold_ok": float((act == cur)[hold].mean()) if hold.any() else float("nan"),
        "mae": float(np.abs(act - intended).mean()),
    }


def make_methods(cfgs, agg_nf, predictor):
    forecaster = LinearForecaster(window=5)
    ts, hpa = ThresholdStateMachine(cfgs), HPA(cfgs)
    ptt = PredictThenThreshold(cfgs, forecaster, predictor, agg_nf)

    def llm(obs, history=None):
        history = history or [0.0]
        fc = forecaster.predict(history)
        pv = violation_prob(float(predictor.predict([fc])[0]), agg_nf.delay_budget)
        payload = build_payload(obs, fc, pv, cfgs)
        return call_llm(payload, cfgs)["actions"]

    return {
        "threshold": ts.decide,
        "hpa": hpa.decide,
        "predict-then-threshold": ptt.decide,
        "llm-stub": llm,
    }

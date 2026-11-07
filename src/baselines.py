"""Non-LLM decision baselines, per slice. Each `decide(obs, history)` returns
a per-slice action dict {slice_type: replicas}."""
from .capacity_model import SLICES, required_replicas


class ThresholdStateMachine:
    def __init__(self, cfgs):
        self.cfgs = cfgs

    def decide(self, obs, history=None):
        act = {}
        for s in SLICES:
            cfg = self.cfgs[s]
            o = obs["slices"][s]
            if o["delay"] > cfg.delay_budget:
                act[s] = required_replicas(o["load"], cfg)
            elif o["delay"] < cfg.delay_budget * 0.5 and o["replicas"] > cfg.min_replicas:
                act[s] = max(cfg.min_replicas, o["replicas"] - 1)
            else:
                act[s] = o["replicas"]
        return act


class HPA:
    def __init__(self, cfgs):
        self.cfgs = cfgs

    def decide(self, obs, history=None):
        return {s: required_replicas(obs["slices"][s]["load"], self.cfgs[s])
                for s in SLICES}


class PredictThenThreshold:
    """Aggregate ML baseline: predict aggregate next load + global violation,
    then scale every slice to required (or hold)."""

    def __init__(self, cfgs, forecaster, predictor, agg_nf):
        self.cfgs = cfgs
        self.forecaster = forecaster
        self.predictor = predictor
        self.agg_nf = agg_nf

    def decide(self, obs, history=None):
        history = history or [0.0]
        pred_load = self.forecaster.predict(history)
        pred_delay = float(self.predictor.predict([pred_load])[0])
        act = {}
        for s in SLICES:
            o = obs["slices"][s]
            if pred_delay > self.agg_nf.delay_budget:
                act[s] = required_replicas(o["load"], self.cfgs[s])
            elif pred_delay < self.agg_nf.delay_budget * 0.5 and o["replicas"] > self.cfgs[s].min_replicas:
                act[s] = max(self.cfgs[s].min_replicas, o["replicas"] - 1)
            else:
                act[s] = o["replicas"]
        return act

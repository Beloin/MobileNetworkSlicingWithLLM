"""Multi-slice replay env (minimal Gymnasium-compatible, no gym dep).

State = {t, slices: {type: {load, replicas, delay, loss}}}.
Action = {slice_type: target_replicas}. `step` clamps each slice to its
NFConfig range and computes per-slice delay/loss via the analytic model.
"""
from .capacity_model import SLICES, delay, loss, violation


class SlicingEnv:
    def __init__(self, states, cfgs, w_viol=10.0, w_cost=0.1, w_change=0.5):
        self.states = states
        self.cfgs = cfgs
        self.w_viol = w_viol
        self.w_cost = w_cost
        self.w_change = w_change
        self.t = 0
        self.replicas = {s: cfgs[s].min_replicas for s in SLICES}

    def _slice(self, s):
        cfg = self.cfgs[s]
        load = self.states[self.t][s]
        d = delay(load, self.replicas[s], cfg)
        l = loss(load, self.replicas[s], cfg)
        return {"load": load, "replicas": self.replicas[s], "delay": d, "loss": l}

    def observe(self):
        return {"t": self.t, "slices": {s: self._slice(s) for s in SLICES}}

    def reset(self):
        self.t = 0
        self.replicas = {s: self.cfgs[s].min_replicas for s in SLICES}
        return self.observe()

    def step(self, action):
        prev = dict(self.replicas)
        for s in SLICES:
            cfg = self.cfgs[s]
            v = action.get(s, prev[s])
            self.replicas[s] = int(round(max(cfg.min_replicas,
                                             min(cfg.max_replicas, v))))
        viol = 0.0
        change = 0.0
        info = {"slices": {}}
        for s in SLICES:
            d, l = delay(self.states[self.t][s], self.replicas[s], self.cfgs[s]), \
                   loss(self.states[self.t][s], self.replicas[s], self.cfgs[s])
            v = 1.0 if violation(d, l, self.cfgs[s]) else 0.0
            viol += v
            change += abs(self.replicas[s] - prev[s])
            info["slices"][s] = {"violation": v, "delay": d, "loss": l}
        cost = sum(self.replicas.values())
        reward = (-self.w_viol * viol
                  - self.w_cost * cost
                  - self.w_change * change)
        obs = self.observe()
        self.t += 1
        done = self.t >= len(self.states)
        return obs, reward, done, info

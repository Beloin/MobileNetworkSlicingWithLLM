"""Next-window load forecasters (Tier 1)."""
import numpy as np


class PersistenceForecaster:
    def predict(self, history):
        return history[-1]


class LinearForecaster:
    def __init__(self, window=5):
        self.window = window

    def predict(self, history):
        w = history[-self.window:]
        if len(w) < 2:
            return w[-1]
        x = np.arange(len(w), dtype=float)
        a, b = np.polyfit(x, w, 1)
        return float(a * len(w) + b)

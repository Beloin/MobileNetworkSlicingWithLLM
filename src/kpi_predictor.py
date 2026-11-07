"""ML baseline: numpy MLP regressor load -> delay.

No sklearn dependency. Trained on dataset (load, delay) pairs. This is the
learned component of the predict-then-threshold baseline; the scaling amount
still comes from the analytic capacity model.
"""
import numpy as np


def _relu(x):
    return np.maximum(x, 0.0)


class MLPRegressor:
    def __init__(self, hidden=16, lr=0.01, epochs=3000, seed=0):
        self.hidden = hidden
        self.lr = lr
        self.epochs = epochs
        self.seed = seed

    def fit(self, X, y):
        X = np.asarray(X, dtype=float).reshape(-1, 1)
        y = np.asarray(y, dtype=float).reshape(-1, 1)
        self.x_mean, self.x_std = float(X.mean()), float(X.std()) + 1e-9
        self.y_mean, self.y_std = float(y.mean()), float(y.std()) + 1e-9
        Xs = (X - self.x_mean) / self.x_std
        ys = (y - self.y_mean) / self.y_std
        rng = np.random.default_rng(self.seed)
        self.W1 = rng.standard_normal((1, self.hidden)) * 0.1
        self.b1 = np.zeros((1, self.hidden))
        self.W2 = rng.standard_normal((self.hidden, 1)) * 0.1
        self.b2 = np.zeros((1, 1))
        n = len(Xs)
        for _ in range(self.epochs):
            h = _relu(Xs @ self.W1 + self.b1)
            out = h @ self.W2 + self.b2
            err = out - ys
            dW2 = h.T @ err / n
            db2 = err.mean(0, keepdims=True)
            dh = err @ self.W2.T
            dh[h <= 0] = 0.0
            dW1 = Xs.T @ dh / n
            db1 = dh.mean(0, keepdims=True)
            self.W2 -= self.lr * dW2
            self.b2 -= self.lr * db2
            self.W1 -= self.lr * dW1
            self.b1 -= self.lr * db1
        return self

    def predict(self, X):
        X = np.asarray(X, dtype=float).reshape(-1, 1)
        Xs = (X - self.x_mean) / self.x_std
        h = _relu(Xs @ self.W1 + self.b1)
        out = (h @ self.W2 + self.b2) * self.y_std + self.y_mean
        return out.ravel()


def violation_prob(pred_delay, budget):
    z = (pred_delay - budget) / (budget + 1e-9)
    return float(1.0 / (1.0 + np.exp(-z)))

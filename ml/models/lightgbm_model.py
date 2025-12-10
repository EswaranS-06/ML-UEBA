# ml/models/lightgbm_model.py

import numpy as np
import joblib

try:
    import lightgbm as lgb
except ImportError:
    lgb = None

from .base import BaseAnomalyModel
from ml.config import LIGHTGBM_PARAMS


class LightGBMAnomalyModel(BaseAnomalyModel):
    """
    Supervised classifier for anomaly vs normal.
    Requires labeled data (0/1). Use when you have GT labels.
    """

    def __init__(self, **params):
        if lgb is None:
            raise ImportError("lightgbm is not installed. Install it to use this model.")
        p = LIGHTGBM_PARAMS.copy()
        p.update(params)
        self.params = p
        self.model = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        train_data = lgb.Dataset(X, label=y)
        self.model = lgb.train(self.params, train_data)
        return self

    def score(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise RuntimeError("Model not trained")
        # Probability of anomaly (class 1)
        proba = self.model.predict(X)
        return np.asarray(proba, dtype="float32")

    def predict_label(self, X: np.ndarray, threshold: float = 0.5):
        scores = self.score(X)
        return (scores >= threshold).astype(int)

    def save(self, path: str):
        if self.model is None:
            raise RuntimeError("No model to save")
        self.model.save_model(path)

    def load(self, path: str):
        self.model = lgb.Booster(model_file=path)
        return self

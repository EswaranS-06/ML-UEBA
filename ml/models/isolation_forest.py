import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from ml.models.base import BaseAnomalyModel
from ml.config import ISOLATION_FOREST_PARAMS

class IsolationForestModel(BaseAnomalyModel):

    def __init__(self):
        self.model = IsolationForest(**ISOLATION_FOREST_PARAMS)

    def fit(self, X):
        self.model.fit(X)

    def score(self, X):
        return -self.model.score_samples(X)

    def save(self, path):
        joblib.dump(self.model, path)

    def load(self, path):
        self.model = joblib.load(path)

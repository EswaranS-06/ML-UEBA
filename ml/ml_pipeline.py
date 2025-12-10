import os
import numpy as np
import pandas as pd

from ml.data_interface import build_feature_matrix
from ml.models.isolation_forest import IsolationForestModel
from ml.models.lstm_autoencoder import LSTMAutoencoder
from ml.models.page_hinkley import PageHinkley
from ml.utils.scaling import load_scaler, transform
from ml.config import MODEL_DIR


class MLPipeline:
    """
    End-to-end ML inference + drift detection pipeline
    """

    def __init__(self):
        self._load_artifacts()

    def _load_artifacts(self):
        # Load scaler
        scaler_path = os.path.join(MODEL_DIR, "scaler.joblib")
        if not os.path.exists(scaler_path):
            raise FileNotFoundError("Scaler not found. Train ML first.")

        self.scaler = load_scaler(scaler_path)

        # Load Isolation Forest
        self.iforest = IsolationForestModel()
        self.iforest.load(os.path.join(MODEL_DIR, "iforest.joblib"))

        # Load LSTM Autoencoder
        self.lstm = LSTMAutoencoder()
        self.lstm.load(os.path.join(MODEL_DIR, "lstm_ae.joblib"))

        # Page-Hinkley drift detector (stateful)
        self.drift = PageHinkley()

    def run(self, df: pd.DataFrame, embeddings: np.ndarray) -> pd.DataFrame:
        if df.empty:
            return df

        # 1. Feature matrix
        X = build_feature_matrix(df, embeddings)

        # 2. Scaling
        X = transform(self.scaler, X)

        # 3. Score models
        if_scores = self.iforest.score(X)
        lstm_scores = self.lstm.score(X)

        # 4. Normalize scores (NumPy 2.0 SAFE)
        if_range = np.ptp(if_scores) + 1e-8
        lstm_range = np.ptp(lstm_scores) + 1e-8

        if_norm = (if_scores - np.min(if_scores)) / if_range
        lstm_norm = (lstm_scores - np.min(lstm_scores)) / lstm_range

        # 5. Ensemble
        anomaly_score = 0.5 * if_norm + 0.5 * lstm_norm

        # 6. Drift detection
        drift_flags = []
        for score in anomaly_score:
            drift_flags.append(self.drift.update(float(score)))

        # 7. Append results
        df_out = df.copy()
        df_out["iforest_score"] = if_scores
        df_out["lstm_score"] = lstm_scores
        df_out["anomaly_score"] = anomaly_score
        df_out["concept_drift"] = drift_flags

        return df_out

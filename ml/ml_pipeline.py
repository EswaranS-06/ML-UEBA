import os
import numpy as np
import pandas as pd

from ml.data_interface import build_feature_matrix
from ml.models.isolation_forest import IsolationForestModel
from ml.models.lstm_autoencoder import LSTMAutoencoder
from ml.models.page_hinkley import PageHinkley
from ml.utils.scaling import load_scaler, transform


class MLPipeline:
    """
    End-to-end ML inference + drift detection pipeline
    """

    def __init__(self):
        # Resolve paths safely (independent of CWD)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(base_dir, ".."))

        self.model_dir = os.path.join(project_root, "models")

        self._load_artifacts()

    def _load_artifacts(self):
        # ---- Scaler ----
        scaler_path = os.path.join(self.model_dir, "scaler.joblib")
        if not os.path.isfile(scaler_path):
            raise FileNotFoundError(
                f"Scaler not found at:\n{scaler_path}\n"
                f"Train ML first before running inference."
            )
        self.scaler = load_scaler(scaler_path)

        # ---- Isolation Forest ----
        iforest_path = os.path.join(self.model_dir, "iforest.joblib")
        if not os.path.isfile(iforest_path):
            raise FileNotFoundError(f"IForest model not found at {iforest_path}")

        self.iforest = IsolationForestModel()
        self.iforest.load(iforest_path)

        # ---- LSTM Autoencoder ----
        lstm_path = os.path.join(self.model_dir, "lstm_ae.joblib")
        if not os.path.isfile(lstm_path):
            raise FileNotFoundError(f"LSTM-AE model not found at {lstm_path}")

        self.lstm = LSTMAutoencoder()
        self.lstm.load(lstm_path)

        # ---- Drift Detector ----
        self.drift = PageHinkley()

        print("[+] ML artifacts loaded successfully")

    def run(self, df: pd.DataFrame, embeddings: np.ndarray) -> pd.DataFrame:
        if df.empty:
            return df

        # 1. Feature matrix
        X = build_feature_matrix(df, embeddings)

        # 2. Scaling
        X = transform(self.scaler, X)

        # 3. Model scores
        if_scores = self.iforest.score(X)
        lstm_scores = self.lstm.score(X)

        # 4. Normalize scores (NumPy 2.0 safe)
        if_range = np.ptp(if_scores) + 1e-8
        lstm_range = np.ptp(lstm_scores) + 1e-8

        if_norm = (if_scores - np.min(if_scores)) / if_range
        lstm_norm = (lstm_scores - np.min(lstm_scores)) / lstm_range

        # 5. Ensemble score
        anomaly_score = 0.5 * if_norm + 0.5 * lstm_norm

        # 6. Drift detection
        drift_flags = [self.drift.update(float(s)) for s in anomaly_score]

        # 7. Append results
        df_out = df.copy()
        df_out["iforest_score"] = if_scores
        df_out["lstm_score"] = lstm_scores
        df_out["anomaly_score"] = anomaly_score
        df_out["concept_drift"] = drift_flags

        return df_out

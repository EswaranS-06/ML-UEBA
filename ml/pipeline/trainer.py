import os
import numpy as np
import pandas as pd

from ml.config import MODEL_DIR
from ml.data_interface import build_feature_matrix
from ml.models.isolation_forest import IsolationForestModel
from ml.models.lstm_autoencoder import LSTMAutoencoder
from ml.utils.scaling import fit_scaler, transform, save_scaler
from ml.utils.io import ensure_dir


def train():
    print("[Trainer] Starting ML training pipeline")

    csv_path = "data/processed/sample.csv"
    emb_path = "data/processed/sample_msg_emb.npy"

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing processed CSV: {csv_path}")
    if not os.path.exists(emb_path):
        raise FileNotFoundError(f"Missing embeddings: {emb_path}")

    df = pd.read_csv(csv_path)
    embeddings = np.load(emb_path)

    print(f"[Trainer] Loaded {len(df)} rows")

    # Build feature matrix
    X = build_feature_matrix(df, embeddings)

    # Scaling
    scaler = fit_scaler(X)
    X_scaled = transform(scaler, X)

    ensure_dir(MODEL_DIR)
    save_scaler(scaler, f"{MODEL_DIR}/scaler.joblib")
    print("[Trainer] Scaler saved")

    # Isolation Forest
    iforest = IsolationForestModel()
    iforest.fit(X_scaled)
    iforest.save(f"{MODEL_DIR}/iforest.joblib")
    print("[Trainer] IsolationForest trained & saved")

    # LSTM Autoencoder
    lstm = LSTMAutoencoder()
    lstm.fit(X_scaled)
    lstm.save(f"{MODEL_DIR}/lstm_ae.joblib")
    print("[Trainer] LSTM Autoencoder trained & saved")

    print("[Trainer] ✅ Training completed successfully")


if __name__ == "__main__":
    train()

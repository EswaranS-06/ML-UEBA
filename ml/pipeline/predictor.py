import numpy as np
from ml.data_interface import build_feature_matrix
from ml.models.isolation_forest import IsolationForestModel
from ml.models.lstm_autoencoder import LSTMAutoencoder
from ml.models.page_hinkley import PageHinkley
from ml.utils.scaling import load_scaler, transform
from ml.utils.io import ensure_dir
from ml.config import MODEL_DIR
import joblib
import os

ensure_dir(MODEL_DIR)

_scaler = load_scaler(f"{MODEL_DIR}/scaler.joblib")
_iforest = IsolationForestModel()
_iforest.load(f"{MODEL_DIR}/iforest.joblib")

_lstm = LSTMAutoencoder()
_lstm.load(f"{MODEL_DIR}/lstm_ae.joblib")

_drift = PageHinkley()

def score_logs(df, embeddings):
    X = build_feature_matrix(df, embeddings)
    X = transform(_scaler, X)

    if_scores = _iforest.score(X)
    lstm_scores = _lstm.score(X)

    if_n = (if_scores - if_scores.min()) / (if_scores.ptp() + 1e-8)
    lstm_n = (lstm_scores - lstm_scores.min()) / (lstm_scores.ptp() + 1e-8)

    anomaly_score = 0.5 * if_n + 0.5 * lstm_n

    drift_flags = [ _drift.update(float(s)) for s in anomaly_score ]

    df_out = df.copy()
    df_out["iforest_score"] = if_scores
    df_out["lstm_score"] = lstm_scores
    df_out["anomaly_score"] = anomaly_score
    df_out["concept_drift"] = drift_flags
    df_out.head(5)
    return df_out

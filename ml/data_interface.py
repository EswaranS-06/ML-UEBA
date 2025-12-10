import numpy as np
import pandas as pd

NUMERIC_FEATURES = [
    "hour", "day_of_week", "is_weekend", "is_working_hour",
    "user_freq", "user_is_rare", "user_event_count", "user_failed_ratio",
    "src_ip_freq", "src_ip_is_rare", "src_ip_is_private", "src_ip_event_count",
    "src_ip_failed_ratio",
    "host_event_count", "host_failed_ratio",
    "process_freq",
    "failed_attempt"
]

def build_feature_matrix(df: pd.DataFrame, embeddings: np.ndarray) -> np.ndarray:
    for col in NUMERIC_FEATURES:
        if col not in df:
            df[col] = 0

    X_struct = df[NUMERIC_FEATURES].fillna(0).astype("float32").values
    X = np.hstack([X_struct, embeddings.astype("float32")])
    return X

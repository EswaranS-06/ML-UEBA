# features/encoders/user_encoder.py

import pandas as pd
import numpy as np


class UserEncoder:
    """
    User-centric features:
      - user_freq: number of events for this user
      - user_is_rare: whether frequency is in bottom X percentile
    """

    def __init__(self, rare_percentile: float = 5.0):
        self.rare_percentile = rare_percentile

    def encode(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "user" not in df.columns:
            df["user_freq"] = 0
            df["user_is_rare"] = 0
            return df

        user_counts = df["user"].fillna("unknown_user").value_counts()
        df["user_freq"] = df["user"].map(user_counts).fillna(0)

        if len(user_counts) > 0:
            threshold = np.percentile(user_counts.values, self.rare_percentile)
        else:
            threshold = 0

        df["user_is_rare"] = (df["user_freq"] < threshold).astype(int)

        return df

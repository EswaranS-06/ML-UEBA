# features/encoders/time_encoder.py

import pandas as pd


class TimeEncoder:
    """
    Encodes timestamp into useful time-based features:
      - hour
      - day_of_week
      - is_weekend
      - is_working_hour
    """

    def encode(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "timestamp" not in df.columns:
            return df

        ts = pd.to_datetime(df["timestamp"], errors="coerce")

        df["hour"] = ts.dt.hour
        df["day_of_week"] = ts.dt.weekday  # 0=Mon
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
        df["is_working_hour"] = df["hour"].between(9, 18).astype(int)

        return df

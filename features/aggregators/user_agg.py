# features/aggregators/user_agg.py

import pandas as pd


class UserAggregator:
    """
    Aggregated user-level features:
      - user_event_count
      - user_failed_ratio
      - user_unique_src_ip
    """

    def aggregate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "user" not in df.columns:
            df["user_event_count"] = 0
            df["user_failed_ratio"] = 0.0
            df["user_unique_src_ip"] = 0
            return df

        user_col = df["user"].fillna("unknown_user")

        # event count per user
        user_counts = user_col.value_counts()
        df["user_event_count"] = user_col.map(user_counts)

        # failed ratio per user
        if "failed_attempt" in df.columns:
            df["user_failed_ratio"] = (
                df.groupby(user_col)["failed_attempt"].transform("mean")
            )
        else:
            df["user_failed_ratio"] = 0.0

        # number of distinct src_ip per user
        if "src_ip" in df.columns:
            tmp = (
                df.groupby("user")["src_ip"]
                .nunique()
                .rename("user_unique_src_ip")
            )
            df = df.join(tmp, on="user")
        else:
            df["user_unique_src_ip"] = 0

        return df

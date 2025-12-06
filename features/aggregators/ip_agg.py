# features/aggregators/ip_agg.py

import pandas as pd


class IPAggregator:
    """
    Aggregated IP-level features (src_ip):
      - src_ip_event_count
      - src_ip_failed_ratio
      - src_ip_unique_users
    """

    def aggregate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "src_ip" not in df.columns:
            df["src_ip_event_count"] = 0
            df["src_ip_failed_ratio"] = 0.0
            df["src_ip_unique_users"] = 0
            return df

        src_col = df["src_ip"].fillna("")

        ip_counts = src_col.value_counts()
        df["src_ip_event_count"] = src_col.map(ip_counts)

        if "failed_attempt" in df.columns:
            df["src_ip_failed_ratio"] = (
                df.groupby(src_col)["failed_attempt"].transform("mean")
            )
        else:
            df["src_ip_failed_ratio"] = 0.0

        if "user" in df.columns:
            tmp = (
                df.groupby("src_ip")["user"]
                .nunique()
                .rename("src_ip_unique_users")
            )
            df = df.join(tmp, on="src_ip")
        else:
            df["src_ip_unique_users"] = 0

        return df

# features/aggregators/host_agg.py

import pandas as pd


class HostAggregator:
    """
    Aggregated host-level features:
      - host_event_count
      - host_failed_ratio
      - host_unique_src_ip
    """

    def aggregate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "host" not in df.columns:
            df["host_event_count"] = 0
            df["host_failed_ratio"] = 0.0
            df["host_unique_src_ip"] = 0
            return df

        host_col = df["host"].fillna("unknown_host")

        # event count per host
        host_counts = host_col.value_counts()
        df["host_event_count"] = host_col.map(host_counts)

        # failed ratio per host
        if "failed_attempt" in df.columns:
            df["host_failed_ratio"] = (
                df.groupby(host_col)["failed_attempt"].transform("mean")
            )
        else:
            df["host_failed_ratio"] = 0.0

        # number of distinct src_ip per host
        if "src_ip" in df.columns:
            tmp = (
                df.groupby("host")["src_ip"]
                .nunique()
                .rename("host_unique_src_ip")
            )
            df = df.join(tmp, on="host")
        else:
            df["host_unique_src_ip"] = 0

        return df

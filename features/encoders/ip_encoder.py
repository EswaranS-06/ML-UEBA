# features/encoders/ip_encoder.py

import pandas as pd
import numpy as np
import ipaddress


class IPEcoder:
    """
    IP-centric features for src_ip:
      - src_ip_freq
      - src_ip_is_rare
      - src_ip_is_private
    """

    def __init__(self, rare_threshold: int = 3):
        self.rare_threshold = rare_threshold

    @staticmethod
    def _is_private_ip(ip: str) -> int:
        try:
            return int(ipaddress.ip_address(ip).is_private)
        except Exception:
            return 0

    def encode(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "src_ip" not in df.columns:
            df["src_ip_freq"] = 0
            df["src_ip_is_rare"] = 0
            df["src_ip_is_private"] = 0
            return df

        src = df["src_ip"].fillna("")

        ip_counts = src.value_counts()
        df["src_ip_freq"] = src.map(ip_counts).fillna(0)

        df["src_ip_is_rare"] = (df["src_ip_freq"] < self.rare_threshold).astype(int)

        df["src_ip_is_private"] = src.apply(self._is_private_ip)

        return df

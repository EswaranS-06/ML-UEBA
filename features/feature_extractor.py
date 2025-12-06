# features/feature_extractor.py

import pandas as pd

from .encoders.time_encoder import TimeEncoder
from .encoders.user_encoder import UserEncoder
from .encoders.ip_encoder import IPEcoder
from .encoders.process_encoder import ProcessEncoder
from .encoders.categorical_encoder import CategoricalEncoder

from .aggregators.user_agg import UserAggregator
from .aggregators.host_agg import HostAggregator
from .aggregators.ip_agg import IPAggregator


class FeatureExtractor:
    """
    Orchestrates feature encoders and aggregators.

    Input:  normalized log DataFrame (from preprocess pipeline)
    Output: DataFrame with additional feature columns
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

        # Encoders
        self.time_encoder = TimeEncoder()
        self.user_encoder = UserEncoder()
        self.ip_encoder = IPEcoder()
        self.process_encoder = ProcessEncoder()
        self.host_encoder = CategoricalEncoder(column="host",
                                               prefix="host",
                                               rare_threshold=5)

        # Aggregators
        self.user_agg = UserAggregator()
        self.host_agg = HostAggregator()
        self.ip_agg = IPAggregator()

    def _log(self, msg: str):
        if self.verbose:
            print(f"[FeatureExtractor] {msg}")

    def _add_basic_flags(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Lightweight derived flags from message.
        """
        df = df.copy()

        if "message" in df.columns:
            msg = df["message"].fillna("")

            # crude but effective fail indicator
            df["failed_attempt"] = msg.str.contains(
                "invalid user|failed|error|closed|denied",
                case=False,
                regex=True
            ).astype(int)
        else:
            df["failed_attempt"] = 0

        return df

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        self._log("Adding basic flags...")
        df = self._add_basic_flags(df)

        self._log("Encoding time features...")
        df = self.time_encoder.encode(df)

        self._log("Encoding user features...")
        df = self.user_encoder.encode(df)

        self._log("Encoding IP features...")
        df = self.ip_encoder.encode(df)

        self._log("Encoding process features...")
        df = self.process_encoder.encode(df)

        self._log("Encoding host categorical features...")
        df = self.host_encoder.encode(df)

        self._log("Computing user-level aggregates...")
        df = self.user_agg.aggregate(df)

        self._log("Computing host-level aggregates...")
        df = self.host_agg.aggregate(df)

        self._log("Computing IP-level aggregates...")
        df = self.ip_agg.aggregate(df)

        return df

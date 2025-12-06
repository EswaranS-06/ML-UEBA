# features/feature_pipeline.py

import pandas as pd

from .feature_extractor import FeatureExtractor


class FeaturePipeline:
    """
    High-level feature engineering pipeline.

    Usage:
        fp = FeaturePipeline()
        df_features = fp.run(df_preprocessed)
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.extractor = FeatureExtractor(verbose=verbose)

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.verbose:
            print("[FeaturePipeline] Starting feature extraction")

        df_out = self.extractor.run(df)

        if self.verbose:
            print("[FeaturePipeline] Feature extraction complete. "
                  f"Shape: {df_out.shape}")

        return df_out

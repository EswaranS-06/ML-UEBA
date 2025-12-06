# features/encoders/categorical_encoder.py

import pandas as pd


class CategoricalEncoder:
    """
    Generic categorical encoder:
      - <prefix>_freq: frequency count
      - <prefix>_id: integer ID (0..N-1)
    """

    def __init__(self, column: str, prefix: str, rare_threshold: int = 1):
        self.column = column
        self.prefix = prefix
        self.rare_threshold = rare_threshold

    def encode(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if self.column not in df.columns:
            df[f"{self.prefix}_freq"] = 0
            df[f"{self.prefix}_id"] = -1
            return df

        col = df[self.column].fillna(f"unknown_{self.column}")

        counts = col.value_counts()
        df[f"{self.prefix}_freq"] = col.map(counts).fillna(0)

        # Integer id mapping
        uniques = list(counts.index)
        id_map = {val: idx for idx, val in enumerate(uniques)}
        df[f"{self.prefix}_id"] = col.map(id_map).fillna(-1).astype(int)

        return df


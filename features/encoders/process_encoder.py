# features/encoders/process_encoder.py

import pandas as pd


class ProcessEncoder:
    """
    Process-centric features:
      - process_freq
      - process_family (e.g. 'ssh', 'cron', 'system')
    """

    def encode(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "process" not in df.columns:
            df["process_freq"] = 0
            df["process_family"] = "unknown"
            return df

        proc = df["process"].fillna("unknown_process")

        counts = proc.value_counts()
        df["process_freq"] = proc.map(counts).fillna(0)

        def classify(p: str) -> str:
            pl = p.lower()
            if "sshd" in pl or "ssh" in pl:
                return "ssh"
            if "cron" in pl:
                return "cron"
            if "systemd" in pl:
                return "systemd"
            if "pam" in pl:
                return "pam"
            return "other"

        df["process_family"] = proc.apply(classify)

        return df

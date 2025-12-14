import sys
import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# backend/core/orchestrator.py

import time
import pandas as pd

from core.metrics import metrics
from storage.postgres_writer import write_events
from storage.log_buffer import add_log

# === IMPORT YOUR EXISTING PIPELINES ===
from preprocess.preprocess_pipeline import PreprocessPipeline
from nlp.nlp_pipeline import NLPPipeline
from features.feature_pipeline import FeaturePipeline
from ml.ml_pipeline import MLPipeline


class Orchestrator:
    """
    Central execution engine:
    Input → Preprocess → NLP → Features → ML → PostgreSQL
    """

    def __init__(self):
        self.preprocess = PreprocessPipeline()
        self.nlp = NLPPipeline()
        self.features = FeaturePipeline()
        self.ml = MLPipeline()

    def process_logs(self, raw_logs: list[str]):
        """
        Process a batch of raw logs
        """

        if not raw_logs:
            return

        start_time = time.time()
        add_log("INFO", f"Processing batch of {len(raw_logs)} logs")

        # =========================
        # 1. PREPROCESS
        # =========================
        df = self.preprocess.run(raw_logs)

        # =========================
        # 2. NLP + EMBEDDINGS
        # =========================
        df, embeddings = self.nlp.run(df)

        # =========================
        # 3. FEATURE ENGINEERING
        # =========================
        df = self.features.run(df)

        # =========================
        # 4. ML INFERENCE
        # =========================
        df = self.ml.run(df, embeddings)

        # =========================
        # 5. WRITE TO POSTGRES
        # =========================
        inserted = write_events(df)

        # =========================
        # 6. METRICS
        # =========================
        metrics["events_processed"] += inserted
        metrics["anomalies"] += int((df["anomaly_score"] > 0.8).sum())
        metrics["logs_per_sec"] = round(
            inserted / max(time.time() - start_time, 1), 2
        )

        add_log(
            "INFO",
            f"Batch completed: {inserted} events written"
        )

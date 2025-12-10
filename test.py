import time
import pandas as pd

import sys, os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from preprocess.preprocess_pipeline import PreprocessPipeline
from nlp.nlp_pipeline import NLPPipeline   # <-- NEW
from features.feature_pipeline import FeaturePipeline
from ml.ml_pipeline import MLPipeline




RAW_PATH = "data/raw/sample.log" 
# RAW_PATH = "data/raw/auth-anomaly.txt" 
PROCESSED_PATH = "data/processed/sample.csv"


def load_raw_logs():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"Raw log file not found: {RAW_PATH}")

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        logs = [line.strip() for line in f if line.strip()]

    print(f"[+] Loaded {len(logs)} logs from {RAW_PATH}")
    return logs


def save_processed(df):
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"[+] Processed logs saved to {PROCESSED_PATH}")


def main():
    logs = load_raw_logs()

    preprocess = PreprocessPipeline()
    nlp = NLPPipeline()   # <-- NLP Block Created    
    features = FeaturePipeline(verbose=True)
    ml = MLPipeline()

    print("\n[+] Parsing and normalizing logs...\n")

    start = time.time()

    # PREPROCESS (parser + normalizer)
    df = preprocess.run(logs)

    # NLP ENRICHMENT (regex-based NER, no LLM)
    print("[+] Running NLP entity extraction (regex + rules)...")
    df, embed = nlp.run(df)
    # Save embeddings for ML training
    #os.makedirs("data/processed", exist_ok=True)
    #import numpy as np
    #np.save("data/processed/sample_msg_emb.npy", embed)
    #print("[+] Message embeddings saved to data/processed/sample_msg_emb.npy")

    #Featuring 
    print("[+] Computing features...")
    df = features.run(df)

    df = ml.run(df, embed)

    end = time.time()

    elapsed = end - start
    per_log = elapsed / max(len(logs), 1)

    save_processed(df)

    print("\n================ TEST SUMMARY ================\n")
    print(df.head())
    print(embed.shape)
    print("\n----------------------------------------------")
    print(f"Total logs processed : {len(logs)}")
    print(f"Total time taken     : {elapsed:.4f} seconds")
    print(f"Average per log      : {per_log:.6f} seconds/log")
    print("==============================================\n")


if __name__ == "__main__":
    main()

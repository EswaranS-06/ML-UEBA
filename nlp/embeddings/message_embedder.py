# nlp/embeddings/message_embedder.py

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import os


class MessageEmbedder:
    """
    Embeds log messages using a locally saved MiniLM model.
    """

    def __init__(self, model_path=None):
        # Resolve path relative to THIS file, not CWD
        base_dir = os.path.dirname(os.path.abspath(__file__))

        if model_path is None:
            model_path = os.path.join(
                base_dir,
                "model",
                "all-MiniLM-L6-v2"
            )

        if not os.path.isdir(model_path):
            raise FileNotFoundError(
                f"SentenceTransformer model not found at:\n{model_path}\n\n"
                f"Fix: run `uv run nlp/embeddings/install_minilm.py`"
            )

        print(f"[+] Loading embeddings model from: {model_path}")

        self.model = SentenceTransformer(model_path)
        self.dim = self.model.get_sentence_embedding_dimension()

    def encode_message(self, text: str):
        if not text:
            return np.zeros(self.dim, dtype=np.float32)

        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def encode_dataframe(self, df: pd.DataFrame, column="message"):
        messages = df[column].fillna("").astype(str).tolist()

        embeddings = self.model.encode(
            messages,
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return embeddings

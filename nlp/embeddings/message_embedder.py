# nlp/embeddings/message_embedder.py

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import os

MODEL_PATH = "nlp/embeddings/model/all-MiniLM-L6-v2"


class MessageEmbedder:
    """
    Embeds log messages using a locally saved MiniLM model.
    """

    def __init__(self, model_path=MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model path not found: {model_path}\n"
                f"Run local_model_setup.py to install the model."
            )

        print(f"[+] Loading embeddings model from: {model_path}")
        self.model = SentenceTransformer(model_path)
        self.dim = self.model.get_sentence_embedding_dimension()

    def encode_message(self, text: str):
        if not text:
            return np.zeros(self.dim, dtype=np.float32)
        return self.model.encode(text)

    def encode_dataframe(self, df: pd.DataFrame, column="message"):
        messages = df[column].fillna("").astype(str).tolist()
        embeddings = self.model.encode(messages, convert_to_numpy=True)
        return embeddings

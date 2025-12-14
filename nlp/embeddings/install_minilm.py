from sentence_transformers import SentenceTransformer
import os

TARGET_DIR = "nlp/embeddings/model/all-MiniLM-L6-v2"

print("[+] Downloading SentenceTransformer model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("[+] Saving model in SentenceTransformer format...")
os.makedirs(TARGET_DIR, exist_ok=True)
model.save(TARGET_DIR)

print("[+] Done. Model saved correctly.")

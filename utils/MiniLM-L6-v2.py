# nlp/embeddings/local_model_setup.py

from sentence_transformers import SentenceTransformer

print("[+] Downloading all-MiniLM-L6-v2 locally...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
model.save("nlp/embeddings/model/all-MiniLM-L6-v2")
print("[+] Saved locally to: nlp/embeddings/model/all-MiniLM-L6-v2")

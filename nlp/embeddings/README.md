# Embeddings Module

The `nlp/embeddings/` package provides **local semantic embeddings** for log messages.  
It uses the **MiniLM (all-MiniLM-L6-v2)** model to generate high-quality vector representations of log text.

These embeddings allow downstream ML models (Isolation Forest, Autoencoder, clustering, UEBA scoring) to detect:

• unusual login attempts  
• strange error messages  
• unseen behavioral patterns  
• new attack signatures  
• rare combinations of actions  

All embeddings are:

• **Fully offline**  
• **Fast** (CPU-friendly)  
• **High-quality**  
• **384-dimensional semantic vectors**  

---

# 📂 Folder Structure

```
nlp/embeddings/
    README.md
    message_embedder.py
    local_model_setup.py
    model/
        all-MiniLM-L6-v2/        (downloaded locally)
```

---

# 🧠 Why Embeddings?

Traditional string matching cannot capture:

• semantic patterns  
• meaning  
• similarity between log messages  
• phrase-level variations  
• unseen attack patterns  

MiniLM embeddings allow the system to numerically represent logs as:

```python
vector shape: (N_logs × 384)
```

These vectors enable:

• anomaly detection  
• clustering  
• correlation of similar events  
• UEBA behavior scoring  

---

# 🧩 message_embedder.py

This file loads the MiniLM model and converts log messages into embeddings.

Example:

```python
from nlp.embeddings.message_embedder import MessageEmbedder

embedder = MessageEmbedder()
emb = embedder.encode_message("Failed password for admin from 1.2.3.4")

print(emb.shape)
# (384,)
```

Batch embedding:

```python
emb_matrix = embedder.encode_dataframe(df, "message")
```

---

# ⚙️ local_model_setup.py

This script downloads MiniLM model locally into:

```
nlp/embeddings/model/all-MiniLM-L6-v2/
```

Run once:

```bash
uv run python nlp/embeddings/local_model_setup.py
```

This ensures:

• no internet required  
• offline and deterministic NLP  
• faster loading times  

---

# 📦 Stored Model

After running setup, you get:

```
nlp/embeddings/model/all-MiniLM-L6-v2/
config.json
pytorch_model.bin
tokenizer.json
modules.json
vocab files
```

The `MessageEmbedder` auto-loads from this path.

---

# 🚀 Usage in Pipeline

Embeddings are integrated inside the main NLP pipeline:

```python
df_enriched, emb_matrix = nlp.run(df_preprocessed)
```

Output:

• df_enriched — enriched DataFrame  
• emb_matrix — array of shape (num_logs, 384)  

Used by:

• Feature Engineering  
• ML Anomaly Models  
• UEBA risk scoring  
• Similarity search engines  

---

# 🧪 Example

Message:

```
Invalid user admin from 187.12.249.74
```

Embedding output:

```python
[ -0.14,  0.22, -0.03, ... ]  # length 384
```

Similar logs have similar embeddings.

---

# 🛠 How to Replace the Model

Modify the model path:

```python
MessageEmbedder(model_path="nlp/embeddings/model/my_model")
```

Supported models:

• MiniLM  
• MPNet  
• DistilBERT  
• Custom fine-tuned models  

---

# 🟢 Summary

The Embeddings Module provides:

✔ Local MiniLM embedding model  
✔ CPU-friendly vectorization  
✔ Batch encoding for log messages  
✔ Drop-in integration with NLP pipeline  
✔ Semantic representation of logs  
✔ Strong foundation for UEBA ML models  

This is a core component for understanding log behavior beyond simple string parsing.


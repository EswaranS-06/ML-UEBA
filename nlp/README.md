# NLP Module

The `nlp/` package provides Natural Language Processing components for log enrichment.  
It operates **after preprocessing** and before feature engineering.

NLP in ML-UEBA focuses on:

1. Extracting entities (username, host, process, IPs)  
2. Recovering missing fields  
3. Cleaning and normalizing message content  
4. Generating **local semantic embeddings** using MiniLM  
5. Providing structured outputs for downstream ML models

---

# 📂 Folder Structure

```
nlp/
    README.md
    nlp_pipeline.py
    regex_extractor.py
    username_classifier.py
    hostname_classifier.py
    process_classifier.py
    network_classifier.py
    ner/
        username_ner.py
    embeddings/
        message_embedder.py
        local_model_setup.py
        model/
            all-MiniLM-L6-v2/ (downloaded locally)
```

---

# 🧠 NLP Overview

The NLP pipeline enhances parsed logs by:

---

## (1) Regex-based Entity Extraction

Fast extraction of:

- Usernames  
- Hosts  
- Processes  
- IPs  
- Ports  

Implemented in:

```python
regex_extractor.py
```

Regex extraction provides high recall and is optimized specifically for system and security logs.

---

## (2) Classifier-Based Post-Processing

Lightweight heuristics decide the **best candidate** among extracted items.

Files:

```python
username_classifier.py
hostname_classifier.py
process_classifier.py
network_classifier.py
```

These add rule-based intelligence to correct fields such as:

- username  
- host name  
- process name  
- source/destination IP  
- source/destination port  

---

## (3) Fallback Username NER

When the parser and regex extraction fail, and:

```python
user == "unknown_user"
```

The NLP pipeline uses:

```python
ner/username_ner.py
```

This is a fast, log-specific NER rule system that detects patterns like:

```
Invalid user admin from 187.12.249.74
Failed password for postgres
authentication failure user=deploy
```

This improves username identification significantly without needing a heavy ML model.

---

## (4) Message Embeddings (MiniLM)

Semantic embeddings are generated for the log message field using:

- `all-MiniLM-L6-v2` (locally downloaded)  
- 384-dimensional vectors  
- CPU-friendly, fast inference  
- Fully offline model execution  

Located in:

```python
embeddings/message_embedder.py
```

Stored in:

```
nlp/embeddings/model/all-MiniLM-L6-v2/
```

Used for:

- Isolation Forest  
- Autoencoders  
- Clustering  
- UEBA scoring  
- Log similarity search  

---

# 🔧 NLP Pipeline

Main file:

```python
nlp_pipeline.py
```

Execution:

```python
from nlp.nlp_pipeline import NLPPipeline

nlp = NLPPipeline()
df_enriched, message_embeddings = nlp.run(df_preprocessed)
```

Pipeline steps:

1. Perform regex extraction  
2. Choose best candidates  
3. Apply fallback NER  
4. Update missing indicators  
5. Generate MiniLM embeddings  

Outputs:

- `df_enriched` → enriched DataFrame  
- `message_embeddings` → NumPy matrix `(N logs × 384 dims)`  

---

# 🧪 Example Output

Input message:

```
Invalid user admin from 122.225.109.208
```

NLP output:

```python
user = "admin"
src_ip = "122.225.109.208"
process = "sshd"
host = "ip-172-31-27-153"
embedding = np.array([...384 dims...])
```

---

# 📦 Local Model Installation

Run once to install MiniLM locally:

```bash
uv run python nlp/embeddings/local_model_setup.py
```

This creates:

```
nlp/embeddings/model/all-MiniLM-L6-v2/
```

No internet needed afterward.

---

# 🧩 How to Extend

## Add a new NER module

1. Create file under `nlp/ner/`  
2. Implement extraction function  
3. Call it in `nlp_pipeline.py`  
4. Update missing handler logic if needed  

## Add a new embedding model

1. Add loader in `message_embedder.py`  
2. Save model locally  
3. Update embedding dimension detection  
4. Update ML workflow if needed  

---

# 🟢 Summary

The NLP module provides:

- High-speed log-oriented entity extraction  
- Intelligent correction of missing fields  
- Lightweight username NER  
- Fully offline MiniLM embeddings  
- A unified enriched DataFrame for ML  

It significantly increases the accuracy of UEBA and anomaly analysis.

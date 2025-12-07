Below is your full text rewritten into **clean, properly formatted Markdown**, with **no content changes** — only structure, spacing, and formatting fixes.

---

# ⚡ ML-UEBA — Machine Learning User & Entity Behavior Analytics

ML-UEBA is a modular, high-performance log analytics and anomaly-detection framework built for:

* Security Operations (SOC)
* Threat Detection
* UEBA (User & Entity Behavior Analytics)
* SIEM enrichment
* Distributed log ingestion environments

The project provides a full pipeline:

```
Raw Logs → Parsing → Normalization → NLP Enrichment → Feature Engineering → Embeddings → ML/Anomaly Detection
```

---

# 🚀 Features

### ✅ Multi-source Log Parsing

Automatically identifies & parses logs from:

* **Linux Syslog**
* **Windows Event Logs**
* **Windows PowerShell**
* **macOS Unified Logs**
* **SSHD logs**
* **RDP logs**
* **PAM logs**
* **Active Directory / Kerberos**
* **CloudTrail**
* **CloudWatch**
* **AWS VPC Flow Logs**
* **GuardDuty**
* **Azure Activity / Firewall / AD Logs**
* **GCP Audit Logs / VPC Flow / IAM**
* **Firewall Logs:** Palo Alto, Fortinet, Cisco ASA
* **IDS/IPS:** Suricata, Zeek, Snort
* **EDR logs**
* **NetFlow / DNS / VPN / Proxy logs**
* **Generic Network Logs**

---

# 🧠 NLP + Entity Extraction

### ✔ Extract usernames, IPs, hosts, processes

### ✔ Regex-based fast extraction

### ✔ Lightweight fallback-NER for missing usernames

### ✔ Sentence-transformer embeddings (MiniLM) for semantic analysis

Embeddings are generated **locally**, fully offline.

---

# 📊 Feature Engineering

The feature layer adds:

* Time features (hour, weekend, working-hours, weekday)
* IP rarity, private/public classification
* User rarity & behavior profiling
* Host behavior profiling
* Process grouping
* Aggregated behavioral metrics:

  * `user_failed_ratio`
  * `user_unique_ips`
  * `host_unique_ips`
  * `src_ip_failed_ratio`
  * `src_ip_unique_users`

Plus optional deep embeddings from NLP.

---

# 🔥 Machine Learning Support

Plugs into:

* **Isolation Forest**
* **Local Outlier Factor**
* **Autoencoders**
* **Sequence Models**
* **Risk Scoring Engines**

---

# 📦 Project Structure

```
ML-UEBA/
│
├── preprocess/                 # Log parsing, normalization, missing handler
├── nlp/                        # NLP pipeline, regex NER, username NER, embeddings
│   └── embeddings/             # MiniLM embeddings (local)
├── features/                   # Feature engineering (encoders, aggregators)
├── config/                     # Parser detection configuration
├── data/                       # Raw & processed logs
├── ml/                         # (optional) anomaly models
├── test.py                     # Run full pipeline on local sample logs
└── README.md
```

---

# 🛠 Installation Guide (uv)

This project uses **uv** — a fast Python package and environment manager.

---

## 1️⃣ Install uv

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:

```powershell
uv --version
```

---

## 2️⃣ Create Project Environment

From project root:

```powershell
uv venv
```

Activate automatically:

```powershell
uv venv --python 3.10

uv run python --version
```

---

## 3️⃣ Install Dependencies

```powershell
uv sync
```

Or manually:

```powershell
uv add pandas numpy pyyaml sentence-transformers scikit-learn
uv add accelerate==0.26.1 transformers
uv pip install torch --index-url https://download.pytorch.org/whl/cpu
```

This avoids compatibility issues.

---

## 4️⃣ Install Local MiniLM Embedding Model

```powershell
uv run python nlp/embeddings/local_model_setup.py
```

This downloads:

```
nlp/embeddings/model/all-MiniLM-L6-v2/
```

Fully offline embedding support.

---

# ▶️ Running the Pipeline

Put logs here:

```bash
data/raw/sample.log
```

Then run:

```powershell
uv run test.py
```

This will:

* Auto-detect log type
* Parse & normalize
* NLP enrich
* Generate MiniLM embeddings
* Compute features
* Save CSV output

---

# 📘 Folder-level READMEs

Each major folder contains its own README:

* `preprocess/README.md`
* `nlp/README.md`
* `features/README.md`
* `nlp/embeddings/README.md`
* `config/README.md`

---

# 🎯 Summary

ML-UEBA is a complete, modular, offline-capable system for:

* Parsing all major log types
* Extracting entities
* Generating embeddings
* Performing UEBA
* Running ML anomaly detection

This makes it suitable for security automation, SIEM augmentation, and academic experimentation.

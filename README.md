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
## Architecture Overview

<p align="center">
  <img src="arc.svg" alt="ML-UEBA Architecture" width="900"/>
</p>

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

---

# 🌐 Web Interface & Agentic AI API

ML-UEBA includes a modern **Control Plane** with an **Agentic AI Consultant** for interactive threat hunting.

### 1️⃣ Install Web Dependencies

The backend requires **FastAPI** to serve the UI and handle API requests.

```powershell
uv add fastapi uvicorn
```
*(Or `pip install fastapi uvicorn`)*

### 2️⃣ Start the Server

Run the unified backend server (serves both Frontend and API):

```powershell
python server.py
# or
uv run python server.py
```

The server will start at: **[http://localhost:8000](http://localhost:8000)**

### 3️⃣ Using the Agentic AI

1.  Navigate to the **Agentic AI** panel in the sidebar.
2.  Select context sources (PostgreSQL, ML Outputs, etc.).
3.  Type a query (e.g., *"Why is this IP anomalous?"*).
4.  The request flows to the backend API:
    *   **Endpoint:** `POST /api/agent/chat`
    *   **Payload:** `{ query: "...", context: { ... } }`

*Note: The current backend implementation (`server.py`) provides intelligent mock responses for demonstration. Connect it to a real LLM by modifying `chat_endpoint` in `server.py`.*




Perfect — below are **clean, readable, ASCII-only architectural diagrams** that you can paste directly into:

- README files
- Docs
- Terminal
- GitHub Markdown

I’ll give you **two diagrams**:

1️⃣ **System Architecture (static view)**

2️⃣ **End-to-End Workflow (runtime / data flow)**

Both are aligned exactly with your current ML-UEBA design.

---

## 1️⃣ ML-UEBA — SYSTEM ARCHITECTURE (ASCII)

```
                           ┌──────────────────────────┐
                           │        FRONTEND          │
                           │  (HTML / CSS / JS)       │
                           │                          │
                           │  - Upload logs           │
                           │  - Configure pipeline    │
                           │  - Start / Stop run      │
                           │  - View metrics          │
                           └───────────┬──────────────┘
                                       │ HTTP (REST API)
                                       ▼
┌────────────────────────────────────────────────────────────────┐
│                          BACKEND (FastAPI)                      │
│                                                                │
│  ┌──────────────┐   ┌──────────────────┐   ┌──────────────┐  │
│  │ API Layer     │──▶│ Pipeline Runner  │──▶│ Orchestrator │  │
│  │ (/api/*)      │   │ (control loop)   │   │ (stages)     │  │
│  └──────────────┘   └──────────────────┘   └──────┬───────┘  │
│                                                      │          │
│  ┌───────────────────────────────────────────────────▼──────┐ │
│  │                   PROCESSING PIPELINE                    │ │
│  │                                                          │ │
│  │  Input → Preprocess → NLP → Features → ML → Storage     │ │
│  │                                                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌─────────────────────┐    ┌──────────────────────────────┐ │
│  │ Log Buffer (memory) │    │ PostgreSQL Writer             │ │
│  │ (UI logs)           │    │ (events table)                │ │
│  └─────────────────────┘    └───────────────┬──────────────┘ │
└──────────────────────────────────────────────┼────────────────┘
                                               │
                                               ▼
                         ┌─────────────────────────────────┐
                         │         POSTGRESQL DB            │
                         │                                 │
                         │  - events                       │
                         │  - anomaly scores               │
                         │  - drift flags                  │
                         └───────────────┬─────────────────┘
                                         │
                     ┌───────────────────▼───────────────────┐
                     │               GRAFANA                  │
                     │        (Dashboards / Visualization)    │
                     └───────────────────────────────────────┘

                     ┌───────────────────────────────────────┐
                     │               ADMINER                  │
                     │        (DB inspection / debug)         │
                     └───────────────────────────────────────┘

```

---

## 2️⃣ ML-UEBA — DATA & WORKFLOW PIPELINE (ASCII)

This shows **what happens when the user clicks “START”**.

```
┌──────────────────────┐
│ User uploads logs    │
│ + config via UI      │
└───────────┬──────────┘
            │
            ▼
┌──────────────────────┐
│ Backend API receives │
│ input + settings     │
└───────────┬──────────┘
            │
            ▼
┌──────────────────────┐
│ PipelineRunner       │
│ starts loop          │
└───────────┬──────────┘
            │
            ▼
┌──────────────────────┐
│ Input Reader         │
│ (file / http / etc.) │
└───────────┬──────────┘
            │ raw logs
            ▼
┌────────────────────────────┐
│ PREPROCESSING               │
│                            │
│ - Detect log type           │
│ - Parse fields              │
│ - Normalize schema          │
│ - Standardize timestamps    │
└───────────┬────────────────┘
            │ DataFrame
            ▼
┌────────────────────────────┐
│ NLP ENRICHMENT              │
│                            │
│ - Regex entity extraction   │
│ - Username recovery         │
│ - Message embeddings        │
└───────────┬────────────────┘
            │ df + embeddings
            ▼
┌────────────────────────────┐
│ FEATURE ENGINEERING         │
│                            │
│ - Time features             │
│ - Frequencies               │
│ - Rarity detection          │
│ - User / Host / IP aggs     │
└───────────┬────────────────┘
            │ feature matrix
            ▼
┌────────────────────────────┐
│ MACHINE LEARNING             │
│                              │
│ - Isolation Forest           │
│ - LSTM Autoencoder           │
│ - Ensemble anomaly score     │
│ - Page-Hinkley drift         │
└───────────┬────────────────┘
            │ enriched df
            ▼
┌────────────────────────────┐
│ STORAGE                     │
│                            │
│ - Write to PostgreSQL       │
│ - Append logs to buffer     │
└───────────┬────────────────┘
            │
            ▼
┌────────────────────────────┐
│ VISUALIZATION               │
│                            │
│ - Grafana dashboards        │
│ - Frontend metrics polling  │
└────────────────────────────┘

```

---

## 3️⃣ RESPONSIBILITY BOUNDARIES (VERY IMPORTANT)

```
Frontend
  └── UI / Control only
      (NO ML, NO parsing)

Backend
  └── Orchestration & APIs
      (NO heavy logic inside routes)

Preprocess / NLP / Features / ML
  └── Pure computation
      (Stateless, reusable, testable)

Storage
  └── Persistence only
      (No business logic)

```

---

## 4️⃣ WHY THIS ARCHITECTURE IS SOLID

✔ Clear separation of concerns

✔ Easy to test each block independently

✔ Scales from file → streaming inputs

✔ Supports UEBA use-cases naturally

✔ No LLM dependency

✔ Production-ready structure

---

If you want next, I can:

- Convert this into **Mermaid diagrams**
- Create a **sequence diagram per API**
- Draw a **Kafka-based future extension**
- Make a **SOC analyst flow diagram**

Just tell me 👍



![arc.svg](attachment:561e2052-ddcb-4f97-97b0-6c527d8c42f4:arc.svg)

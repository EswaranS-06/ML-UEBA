# Helper Backend API Specification

This document details all API endpoints required by the frontend application. The backend should handle these requests to ensure full functionality of the UI.

**Base URL:** `http://localhost:8000/api`

---

## 1. Input Panel

### 1.1 Upload Files
**Endpoint:** `POST /input/upload`
**Content-Type:** `multipart/form-data`

**Request:**
- `files`: One or more file objects (logs, text files).

**Response:**
```json
{
  "message": "Files uploaded successfully",
  "files_processed": 3
}
```

### 1.2 Save Input Configuration
**Endpoint:** `POST /input/config`
**Content-Type:** `application/json`

**Request (Kafka):**
```json
{
  "type": "kafka",
  "bootstrap_servers": "localhost:9092",
  "topic": "auth-logs",
  "group_id": "ueba-consumer"
}
```

**Request (HTTP Source):**
```json
{
  "type": "http",
  "port": 8080,
  "auth_token": "secret-token-123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Input configuration saved"
}
```

---

## 2. Pipeline Configuration

### 2.1 Save Pipeline Settings
**Endpoint:** `POST /pipeline/config`
**Content-Type:** `application/json`

**Request:**
```json
{
  "preprocessing": {
    "enabled": true,
    "parsing": true,
    "feature_engineering": false
  },
  "nlp": {
    "username_recovery": true,
    "entity_enrichment": false,
    "embeddings": true
  },
  "models": {
    "isolation_forest": true,
    "lstm": false
  },
  "drift": {
    "page_hinkley": true
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Pipeline configuration updated"
}
```

---

## 3. Output Configuration

### 3.1 Save Output Settings
**Endpoint:** `POST /output/config`
**Content-Type:** `application/json`

**Request:**
```json
{
  "storage": {
    "postgres": true
  },
  "outputs": [
    {
      "type": "file_download",
      "format": "csv" 
    },
    {
      "type": "kafka",
      "topic": "anomalies-topic"
    },
    {
      "type": "elasticsearch",
      "index": "ueba-results"
    },
    {
      "type": "webhook",
      "url": "https://hooks.slack.com/..."
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Output outputs configured"
}
```

---

## 4. Run Control & Status

### 4.1 Control Pipeline
**Endpoint:** `POST /run/{action}`
**Actions:** `start`, `pause`, `stop`

**Request:** `POST /run/start` (Empty Body)

**Response:**
```json
{
  "status": "success",
  "message": "Pipeline started",
  "current_state": "RUNNING"
}
```

### 4.2 Fetch Metrics (Polled)
**Endpoint:** `GET /run/metrics`

**Response:**
```json
{
  "status": "RUNNING", 
  "logs_per_sec": 128,
  "events_processed": 5420,
  "anomalies": 12,
  "drift_detected": false
}
```
*Note: `status` can be "RUNNING", "PAUSED", "STOPPED".*

---

## 5. Database Status

### 5.1 Fetch Database Stats (Polled)
**Endpoint:** `GET /database/stats`

**Response:**
```json
{
  "connected": true,
  "host": "postgres:5432",
  "database": "ueba_prod",
  "user": "admin",
  "rows_events": 15400,
  "rows_risk": 320,
  "last_insert": "2025-12-13 10:00:00",
  "grafana_connected": true
}
```
*If backend is down or DB unreachable, ensure to return appropriate HTTP errors or `connected: false`.*

---

## 6. Logs

### 6.1 Fetch Live Logs (Polled)
**Endpoint:** `GET /logs`
**Query Param:** `?after_id={integer}` (Optional, for incremental fetching)

**Response:**
```json
{
  "logs": [
    {
      "id": 101,
      "timestamp": "2025-12-13T10:05:00Z",
      "level": "INFO", 
      "message": "Pipeline started successfully"
    },
    {
      "id": 102,
      "timestamp": "2025-12-13T10:05:01Z",
      "level": "WARN",
      "message": "High memory usage detected"
    }
  ]
}
```

---

## CORS Note
Ensure the backend allows CORS from the frontend origin (typically `http://localhost:5500` or `127.0.0.1:5500` during development).

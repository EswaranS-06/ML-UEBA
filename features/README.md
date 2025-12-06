# Feature Engineering Module

The `features/` package transforms normalized & NLP-enriched logs into **numerical feature vectors** suitable for machine learning:

Raw Logs → Preprocess → NLP → Feature Engineering → ML Model

This module produces:

• Behavioral features  
• Frequency features  
• Rare-entity features  
• Temporal features  
• Aggregated user/IP/host statistics  
• Categorical encodings  
• IP-specific features  

These outputs are consumed by ML models (IsolationForest, Autoencoders, Clustering, UEBA scoring).

---

# 📂 Folder Structure

```
features/
    README.md
    feature_pipeline.py
    feature_extractor.py
    encoders/
        __init__.py
        categorical_encoder.py
        time_encoder.py
        user_encoder.py
        host_encoder.py
        process_encoder.py
        ip_encoder.py
    aggregators/
        __init__.py
        user_agg.py
        host_agg.py
        ip_agg.py
```

Each category is modular and independently extendable.

---

# 🧠 Overview

The Feature Engineering stage enhances logs with:

---

## 1. Time-based features

Extracted by `time_encoder.py`:

• hour  
• weekday  
• weekend  
• working-hours flag  
• day_of_month  

Example:

```python
df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
df["is_weekend"] = df["weekday"].isin([5, 6]).astype(int)
```

---

## 2. User behavior features

From `user_encoder.py`:

• user frequency  
• user rarity score  
• number of unique IPs per user  
• typical event volume per user  

Used to detect:

• compromised accounts  
• impossible travel conditions  
• abnormal user activity spikes  

---

## 3. Host behavior features

From `host_encoder.py`:

• host frequency  
• host anomaly metrics  
• host-user interaction patterns  

Used for detecting:

• privilege escalation  
• lateral movement  
• host compromise  
• brute-force activity  

---

## 4. Process behavior features

From `process_encoder.py`:

• process frequency  
• process rarity  
• grouping (e.g., sshd → auth_category)  

This helps detect unusual processes running on a host.

---

## 5. IP-based features

From `ip_encoder.py`:

• frequency of source IP  
• IP rarity  
• public/private IP classification  
• source IP failed login ratio  
• interactions between user/IP and host/IP  

Useful for:

• brute-force attacks  
• suspicious geographic activity  
• compromised hosts  
• scanning or reconnaissance  

---

# 🔁 6. Aggregation Features

Aggregation is key in UEBA.

### Implemented in:

* `user_agg.py`  
* `host_agg.py`  
* `ip_agg.py`  

### Aggregates include:

• user_failed_ratio  
• ip_failed_ratio  
• host_failed_ratio  
• user_unique_ips  
• ip_unique_users  
• host_unique_users  
• average events per hour  
• anomaly-heavy windows  

Example:

```python
df["user_failed_ratio"] = (
    df.groupby("user")["failed_attempt"].transform("mean")
)
```

These metrics allow ML models to detect **pattern anomalies**, not just event anomalies.

---

# 🧩 feature_extractor.py

This file orchestrates all encoders and aggregators.

Internal steps:

```python
df = self.time_encoder.apply(df)
df = self.user_encoder.apply(df)
df = self.host_encoder.apply(df)
df = self.process_encoder.apply(df)
df = self.ip_encoder.apply(df)
df = self.aggregator_user.apply(df)
df = self.aggregator_host.apply(df)
df = self.aggregator_ip.apply(df)
```

Outputs a **numeric-feature-rich DataFrame**.

---

# 🔗 feature_pipeline.py

The FeaturePipeline connects NLP → Features → ML.

Typical usage:

```python
from features.feature_pipeline import FeaturePipeline

fp = FeaturePipeline()
df_features = fp.run(df_enriched)
```

Returned object:

• DataFrame with selected numerical features  
• Safe for input into  
  – IsolationForest  
  – LOF  
  – Autoencoder  
  – Clustering  
  – UEBA risk scoring  

---

# 🧪 Example Input → Output

Input (from NLP):

```python
timestamp, user, src_ip, process, host, message
```

After Feature Engineering:

```python
hour
weekday
is_weekend
user_freq
user_is_rare
host_freq
process_freq
src_ip_freq
src_ip_is_rare
user_failed_ratio
ip_failed_ratio
host_failed_ratio
user_unique_ips
ip_unique_users
```

This structured representation is ideal for anomaly detection.

---

# 🛠️ Extending the Feature Module

## Add a new feature encoder:

1. Create a new file in `features/encoders/`  
2. Implement `apply(self, df)`  
3. Register in `feature_extractor.py`  
4. Add to FeaturePipeline  

## Add a new aggregation:

1. Add new aggregator in `features/aggregators/`  
2. Implement `apply(self, df)`  
3. Register inside `feature_extractor.py`  

---

# 🟢 Summary

The Feature Engineering module is responsible for:

✔ Behavioral analytics  
✔ Rare entity detection  
✔ Time-based pattern learning  
✔ User/IP/Host interaction modeling  
✔ Producing ML-ready numerical features  

This is the backbone of the UEBA anomaly detection engine.


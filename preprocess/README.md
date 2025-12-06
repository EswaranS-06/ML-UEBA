# Preprocess Module

The `preprocess/` package contains all components related to:

1. **Log type detection**  
2. **Parsing raw logs**  
3. **Normalization and cleaning**  
4. **Missing value handling**  
5. **Returning a unified schema for the NLP and Feature pipelines**

This is the first stage of the ML-UEBA pipeline.

---

## 📂 Folder Structure

```
preprocess/
    README.md
    parser_registry.py
    preprocess_pipeline.py
    normalizer/
        timestamp_normalizer.py
        missing_handler.py
        field_standardizer.py
    parsers/
        syslog_parser.py
        windows_parser.py
        cloudtrail_parser.py
        network_parser.py
        base_parser.py
```

---

# 🔍 Overview

```
Raw logs → ParserRegistry → Selected Parser → Normalizer → DataFrame
```

Each log is:

- Auto-detected (syslog, windows, network, cloudtrail, etc.)  
- Parsed via the correct parser  
- Normalized into a common schema  
- Cleaned  
- Assigned missing-indicator fields  
- Returned as a Pandas DataFrame  

---

# 🧠 Unified Log Schema (Output)

Every parser must output this structure:

```python
{
    "timestamp": str or None,
    "epoch_timestamp": int or None,
    "user": str or None,
    "src_ip": str or None,
    "dest_ip": str or None,
    "process": str or None,
    "host": str or None,
    "source": str,         # replaces event_type
    "message": str,
    "raw": str,            # original log string
    "has_user": int,
    "has_src_ip": int,
    "has_dest_ip": int,
    "has_process": int,
    "has_host": int,
    "has_message": int
}
```

---

# 🏗️ Main Components

## 1. ParserRegistry  
**File:** `preprocess/parser_registry.py`

Responsible for:

- Matching raw log strings or dicts to the correct parser  
- Using rules defined in `config/parser_config.yml`  
- Supporting text, regex, and dict-based triggers  
- Returning the appropriate parser class  

Example usage:

```python
registry = ParserRegistry()
ptype = registry.detect_type(log_line)
parser = registry.get_parser(ptype)
parsed = parser.parse(log_line)
```

---

## 2. PreprocessPipeline  
**File:** `preprocess/preprocess_pipeline.py`

Executes the full pipeline for a batch of logs:

```python
pipeline = PreprocessPipeline()
df = pipeline.run(logs)
```

Pipeline includes:

- Parsing (ParserRegistry)  
- Timestamp normalization  
- Missing value filling  
- Indicator fields  
- Returning a clean DataFrame  

---

## 3. Normalizers

### a. TimestampNormalizer  
Converts timestamps such as:

```
Nov 30 08:42:04
2025-11-30T05:28:27Z
2023-10-21 14:55:22
```

Into both:

- ISO8601 timestamp  
- `epoch_timestamp`  

---

### b. MissingHandler  

Ensures consistent fallbacks:

```
user      → unknown_user
host      → unknown_host
process   → unknown_process
src_ip    → None
dest_ip   → None
message   → ""
```

And adds:

```
has_user
has_src_ip
has_dest_ip
has_process
has_host
has_message
```

---

### c. FieldStandardizer  

Ensures naming consistency across parsers  
(every parser can output raw fields, and this module standardizes them).

---

## 4. Parsers

Located in `preprocess/parsers/`:

- SyslogParser  
- WindowsParser  
- CloudTrailParser  
- NetworkParser  
- BaseParser (interface)  

Each parser implements:

```python
def parse(self, raw_log) -> dict:
    ...
```

And maps fields into the unified schema.

---

# 🧪 Example

**Raw syslog input:**

```
Nov 30 10:58:27 ip-172-31-27-153 sshd[22291]: Invalid user admin from 122.225.109.208
```

**After preprocess:**

```python
{
    "timestamp": "2025-11-30T10:58:27+00:00",
    "epoch_timestamp": 1764480507,
    "user": "unknown_user",
    "src_ip": "122.225.109.208",
    "dest_ip": None,
    "process": "sshd[22291]",
    "host": "ip-172-31-27-153",
    "source": "syslog",
    "message": "Invalid user admin from 122.225.109.208",
    "raw": "...",
    "has_user": 0,
    "has_src_ip": 1,
    "has_process": 1,
    "has_host": 1,
    "has_message": 1
}
```

---

# 🔧 How to Extend

### Add a new parser

1. Create `new_parser.py` inside `preprocess/parsers/`  
2. Implement `.parse()` following `BaseParser`  
3. Add detection rules to `config/parser_config.yml`  
4. Register in `parser_registry.py` under `available_parsers`  

---

# 🟢 Summary

The preprocess module:

✔ Detects log type  
✔ Parses raw logs  
✔ Normalizes fields  
✔ Handles missing data  
✔ Produces a clean structured DataFrame  

It is the foundation of the entire ML-UEBA pipeline.


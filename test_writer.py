import pandas as pd
import psycopg2
import psycopg2.extras
import math

CSV_PATH = "data/processed/sample.csv"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "ueba",
    "user": "ueba",
    "password": "ueba",
}

TABLE = "events"


# Explicit CSV → DB column mapping
COLUMN_MAP = {
    "timestamp": "timestamp",
    "epoch_timestamp": "epoch_timestamp",

    "user": "user_name",
    "host": "host",
    "process": "process",

    "src_ip": "src_ip",
    "dest_ip": "dest_ip",
    "src_port": "src_port",
    "dst_port": "dst_port",
    "protocol": "protocol",

    "bytes_in": "bytes_in",
    "bytes_out": "bytes_out",

    "source": "source",
    "message": "message",
    "raw": "raw",

    "has_user": "has_user",
    "has_src_ip": "has_src_ip",
    "has_process": "has_process",
    "has_host": "has_host",
    "has_dest_ip": "has_dest_ip",
    "has_message": "has_message",
    "has_src_port": "has_src_port",
    "has_dst_port": "has_dst_port",
    "has_protocol": "has_protocol",

    "failed_attempt": "failed_attempt",

    "hour": "hour",
    "day_of_week": "day_of_week",
    "is_weekend": "is_weekend",
    "is_working_hour": "is_working_hour",

    "user_freq": "user_freq",
    "user_is_rare": "user_is_rare",

    "src_ip_freq": "src_ip_freq",
    "src_ip_is_rare": "src_ip_is_rare",
    "src_ip_is_private": "src_ip_is_private",

    "process_freq": "process_freq",
    "process_family": "process_family",

    "host_freq": "host_freq",

    "user_event_count": "user_event_count",
    "user_failed_ratio": "user_failed_ratio",
    "user_unique_src_ip": "user_unique_src_ip",

    "host_event_count": "host_event_count",
    "host_failed_ratio": "host_failed_ratio",
    "host_unique_src_ip": "host_unique_src_ip",

    "src_ip_event_count": "src_ip_event_count",
    "src_ip_failed_ratio": "src_ip_failed_ratio",
    "src_ip_unique_users": "src_ip_unique_users",

    "iforest_score": "iforest_score",
    "lstm_score": "lstm_score",
    "anomaly_score": "anomaly_score",
    "concept_drift": "concept_drift",
}

BOOLEAN_COLS = {
    "has_user",
    "has_src_ip",
    "has_process",
    "has_host",
    "has_dest_ip",
    "has_message",
    "has_src_port",
    "has_dst_port",
    "has_protocol",
    "failed_attempt",
    "is_weekend",
    "is_working_hour",
    "user_is_rare",
    "src_ip_is_rare",
    "src_ip_is_private",
    "concept_drift",
}


def clean_value(v, col):
    if v is None:
        return None

    if isinstance(v, float) and math.isnan(v):
        return None

    if col in BOOLEAN_COLS:
        return bool(v)

    return v


def main():
    print("[*] Loading CSV:", CSV_PATH)
    df = pd.read_csv(CSV_PATH)
    print(f"[*] Loaded {len(df)} rows")

    # HARD DROP forbidden column
    if "host_id" in df.columns:
        df = df.drop(columns=["host_id"])

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("[*] Starting row-by-row insertion test...\n")

    for i, row in df.iterrows():
        record = {}

        for csv_col, db_col in COLUMN_MAP.items():
            val = row.get(csv_col)

            if db_col == "raw":
                record[db_col] = psycopg2.extras.Json(
                    {} if val is None else {"raw": str(val)}
                )
            else:
                record[db_col] = clean_value(val, csv_col)

        cols = list(record.keys())
        vals = [record[c] for c in cols]

        placeholders = ",".join(["%s"] * len(cols))
        col_sql = ",".join(cols)

        query = f"""
            INSERT INTO {TABLE} ({col_sql})
            VALUES ({placeholders})
        """

        try:
            cur.execute(query, vals)
            conn.commit()
        except Exception as e:
            print("🚨 INSERT FAILED")
            print(f"Row index : {i}")
            print(f"Error     : {e}\n")
            print("Column diagnostics:")
            for c, v in record.items():
                print(f"  {c:<25} | {type(v)} | {v}")
            conn.rollback()
            break

    cur.close()
    conn.close()
    print("✅ Test insertion completed")


if __name__ == "__main__":
    main()

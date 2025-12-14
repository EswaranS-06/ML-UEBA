from storage.postgres import get_conn
import psycopg2.extras
import math


# Explicit mapping: DataFrame column -> DB column
# NOTE: host_id is intentionally NOT included
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


BOOLEAN_COLUMNS = {
    "has_user",
    "has_src_ip",
    "has_dest_ip",
    "has_process",
    "has_host",
    "has_message",
    "has_src_port",
    "has_dst_port",
    "has_protocol",

    "is_weekend",
    "is_working_hour",

    "user_is_rare",
    "src_ip_is_rare",
    "src_ip_is_private",

    "failed_attempt",
    "concept_drift",
}


def _clean_value(val, db_col):
    """Normalize Python / pandas values to PostgreSQL-safe values."""
    if val is None:
        return None

    if isinstance(val, float) and math.isnan(val):
        return None

    if db_col in BOOLEAN_COLUMNS:
        return bool(val)

    return val


def write_events(df):
    """
    Writes processed events to PostgreSQL.
    This function mirrors test_writer.py behavior exactly.
    """

    if df.empty:
        return 0

    # 🔒 HARD SAFETY: never allow host_id to reach DB
    if "host_id" in df.columns:
        df = df.drop(columns=["host_id"])

    values = []

    for _, row in df.iterrows():
        record = {}

        for df_col, db_col in COLUMN_MAP.items():
            val = row.get(df_col)

            if db_col == "raw":
                record[db_col] = psycopg2.extras.Json(
                    {} if val is None else {"raw": str(val)}
                )
            else:
                record[db_col] = _clean_value(val, db_col)

        values.append(record)

    if not values:
        return 0

    db_columns = list(values[0].keys())

    query = f"""
        INSERT INTO events ({",".join(db_columns)})
        VALUES %s
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            psycopg2.extras.execute_values(
                cur,
                query,
                [tuple(v[c] for c in db_columns) for v in values],
                page_size=500
            )

    return len(values)

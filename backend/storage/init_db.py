from storage.postgres import get_conn

CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS events (
  id SERIAL PRIMARY KEY,

  timestamp TIMESTAMPTZ,
  epoch_timestamp BIGINT,

  user_name TEXT,
  host TEXT,
  process TEXT,

  src_ip INET,
  dest_ip INET,
  src_port INT,
  dst_port INT,
  protocol TEXT,

  bytes_in BIGINT,
  bytes_out BIGINT,

  source TEXT,
  message TEXT,
  raw JSONB,

  has_user BOOLEAN,
  has_src_ip BOOLEAN,
  has_process BOOLEAN,
  has_host BOOLEAN,
  has_dest_ip BOOLEAN,
  has_message BOOLEAN,
  has_src_port BOOLEAN,
  has_dst_port BOOLEAN,
  has_protocol BOOLEAN,

  failed_attempt BOOLEAN,

  hour INT,
  day_of_week INT,
  is_weekend BOOLEAN,
  is_working_hour BOOLEAN,

  user_freq INT,
  user_is_rare BOOLEAN,

  src_ip_freq INT,
  src_ip_is_rare BOOLEAN,
  src_ip_is_private BOOLEAN,

  process_freq INT,
  process_family TEXT,

  host_freq INT,
  host_id INT,

  user_event_count INT,
  user_failed_ratio FLOAT,
  user_unique_src_ip INT,

  host_event_count INT,
  host_failed_ratio FLOAT,
  host_unique_src_ip INT,

  src_ip_event_count INT,
  src_ip_failed_ratio FLOAT,
  src_ip_unique_users INT,

  iforest_score FLOAT,
  lstm_score FLOAT,
  anomaly_score FLOAT,
  concept_drift BOOLEAN
);
"""

def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_EVENTS_TABLE)
            print("[DB] events table ready")

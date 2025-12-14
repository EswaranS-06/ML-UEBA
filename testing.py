import pandas as pd
from backend.storage.postgres_writer import write_events

df = pd.DataFrame([{
    "timestamp": "2025-12-14T00:00:00Z",
    "epoch_timestamp": 1764480000,
    "user": "test_user",
    "host": "test_host",
    "process": "sshd",
    "message": "test message",
    "raw": {}
}])

print(write_events(df))

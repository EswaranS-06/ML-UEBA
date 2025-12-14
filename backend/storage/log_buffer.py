from collections import deque
from datetime import datetime

log_buffer = deque(maxlen=1000)
log_id = 0


def add_log(level: str, message: str):
    global log_id
    log_id += 1
    log_buffer.append({
        "id": log_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "message": message
    })


def get_logs(after_id=None):
    if after_id is None:
        return list(log_buffer)
    return [l for l in log_buffer if l["id"] > after_id]

from fastapi import APIRouter
from storage.postgres import get_conn

router = APIRouter()


@router.get("/stats")
def get_db_stats():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM events")
                rows_events = cur.fetchone()[0]

                cur.execute("SELECT MAX(timestamp) FROM events")
                last_insert = cur.fetchone()[0]

        return {
            "connected": True,
            "host": "localhost:5432",
            "database": "ueba",
            "user": "ueba",
            "rows_events": rows_events,
            "rows_risk": 0,
            "last_insert": last_insert,
            "grafana_connected": True
        }

    except Exception as e:
        return {
            "connected": False,
            "error": str(e)
        }

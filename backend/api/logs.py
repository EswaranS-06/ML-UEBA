from fastapi import APIRouter
from storage.log_buffer import get_logs

router = APIRouter()


@router.get("/")
def fetch_logs(after_id: int | None = None):
    return {
        "logs": get_logs(after_id)
    }

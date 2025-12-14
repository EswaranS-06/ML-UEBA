from fastapi import APIRouter
from config.pipeline_config import pipeline_config
from storage.log_buffer import add_log

router = APIRouter()


@router.post("/config")
def save_pipeline_config(config: dict):
    pipeline_config.update(config)
    add_log("INFO", "Pipeline configuration updated")

    return {
        "status": "success",
        "message": "Pipeline configuration updated"
    }

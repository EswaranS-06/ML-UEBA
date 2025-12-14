from fastapi import APIRouter
from config.output_config import output_config
from storage.log_buffer import add_log

router = APIRouter()


@router.post("/config")
def save_output_config(config: dict):
    # Enforce PostgreSQL always on
    config["storage"]["postgres"] = True
    output_config.update(config)

    add_log("INFO", "Output configuration saved")

    return {
        "status": "success",
        "message": "Output outputs configured"
    }

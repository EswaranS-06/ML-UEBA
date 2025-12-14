# backend/api/run.py

from fastapi import APIRouter

from core.pipeline_state import pipeline_state
from core.metrics import metrics
from core.pipeline_runner import PipelineRunner
from inputs.file_input import FileInput
from storage.log_buffer import add_log

router = APIRouter()

from core.input_state import input_state
from inputs.file_input import FileInput

runner = None

@router.post("/{action}")
def control_pipeline(action: str):
    global runner

    if action == "start":
        if input_state.input_type != "file" or not input_state.file_path:
            return {
                "status": "error",
                "message": "No input file configured"
            }

        input_reader = FileInput(input_state.file_path)
        runner = PipelineRunner(input_reader)

        pipeline_state.start()
        metrics["status"] = "RUNNING"

        runner.start()

        add_log("INFO", "Pipeline started with uploaded file")

    elif action == "pause":
        pipeline_state.pause()
        metrics["status"] = "PAUSED"

    elif action == "stop":
        pipeline_state.stop()
        metrics["status"] = "STOPPED"
        runner.stop()

    add_log("INFO", f"Pipeline {action}")

    return {
        "status": "success",
        "message": f"Pipeline {action}ed",
        "current_state": pipeline_state.state
    }


@router.get("/metrics")
def get_metrics():
    return metrics

from fastapi import APIRouter, UploadFile, File
from typing import List
import os
from storage.log_buffer import add_log
from core.input_state import input_state

router = APIRouter()

UPLOAD_DIR = "data/uploads"


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    saved_files = []

    for f in files:
        save_path = os.path.join(UPLOAD_DIR, f.filename)

        with open(save_path, "wb") as out:
            out.write(await f.read())

        saved_files.append(save_path)

    # For now: use the FIRST uploaded file as input
    if saved_files:
        input_state.set_file(saved_files[0])
        add_log("INFO", f"Active input file set to {saved_files[0]}")

    add_log("INFO", f"{len(saved_files)} files uploaded")

    return {
        "message": "Files uploaded successfully",
        "files_processed": len(saved_files),
        "active_file": saved_files[0] if saved_files else None
    }



@router.post("/config")
async def save_input_config(config: dict):
    input_config.update(config)
    add_log("INFO", "Input configuration saved")

    return {
        "status": "success",
        "message": "Input configuration saved"
    }

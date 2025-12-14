from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import input, pipeline, output, run, database, logs

app = FastAPI(title="ML-UEBA Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(input.router, prefix="/api/input")
app.include_router(pipeline.router, prefix="/api/pipeline")
app.include_router(output.router, prefix="/api/output")
app.include_router(run.router, prefix="/api/run")
app.include_router(database.router, prefix="/api/database")
app.include_router(logs.router, prefix="/api/logs")

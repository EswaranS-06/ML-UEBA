# backend/core/pipeline_runner.py

import threading
import time

from core.pipeline_state import pipeline_state
from core.orchestrator import Orchestrator
from storage.log_buffer import add_log


class PipelineRunner:
    def __init__(self, input_reader):
        self.input_reader = input_reader
        self.orchestrator = Orchestrator()
        self.thread = None
        self.running = False

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self.run_loop, daemon=True)
        self.thread.start()
        add_log("INFO", "Pipeline runner started")

    def stop(self):
        self.running = False
        add_log("INFO", "Pipeline runner stopped")

    def run_loop(self):
        add_log("INFO", "Pipeline loop entered")

        while self.running:
            try:
                if pipeline_state.state != "RUNNING":
                    time.sleep(1)
                    continue

                add_log("DEBUG", "Reading batch from input")

                raw_logs = self.input_reader.read_batch()

                if not raw_logs:
                    add_log("INFO", "No more logs to process (input empty)")
                    time.sleep(2)
                    continue

                add_log("INFO", f"Processing {len(raw_logs)} logs")
                self.orchestrator.process_logs(raw_logs)

            except Exception as e:
                add_log("ERROR", f"Pipeline error: {e}")
                time.sleep(2)


class PipelineState:
    def __init__(self):
        self.state = "STOPPED"

    def start(self):
        self.state = "RUNNING"

    def pause(self):
        self.state = "PAUSED"

    def stop(self):
        self.state = "STOPPED"


pipeline_state = PipelineState()

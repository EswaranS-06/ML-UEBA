# backend/core/input_state.py

class InputState:
    def __init__(self):
        self.input_type = None
        self.file_path = None

    def set_file(self, path: str):
        self.input_type = "file"
        self.file_path = path


input_state = InputState()

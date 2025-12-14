# backend/inputs/file_input.py

import os


class FileInput:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.offset = 0

        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"Input file not found: {self.file_path}")


    def read_batch(self, batch_size=50):
        logs = []

        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = lines[self.offset:self.offset + batch_size]
        self.offset += len(new_lines)

        for line in new_lines:
            line = line.strip()
            if line:
                logs.append(line)

        return logs

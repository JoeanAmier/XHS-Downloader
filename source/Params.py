from pathlib import Path


class Params:
    def __init__(self, path: str):
        self.path = Path(path)

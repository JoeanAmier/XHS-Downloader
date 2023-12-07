from json import dump
from json import load
from pathlib import Path

__all__ = ['Settings']


class Settings:
    default = {
        "path": "",
        "folder_name": "Download",
        "user_agent": "",
        "proxy": "",
        "timeout": 10,
        "chunk": 1024 * 1024,
        "max_retry": 5,
    }

    def __init__(self, root: Path):
        self.file = root.joinpath("./settings.json")

    def run(self):
        return self.read() if self.file.is_file() else self.create()

    def read(self) -> dict:
        with self.file.open("r", encoding="utf-8") as f:
            return load(f)

    def create(self) -> dict:
        with self.file.open("w", encoding="utf-8") as f:
            dump(self.default, f, indent=4)
            return self.default

    def update(self, data: dict):
        with self.file.open("w", encoding="utf-8") as f:
            dump(data, f, indent=4, ensure_ascii=False)

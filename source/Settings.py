from json import dump
from json import load
from pathlib import Path


class Settings:
    path = Path("./settings.json")
    default = {
        "path": "./",
        "folder": "Download",
        "proxies": None,
        "timeout": 10,
        "chunk": 256 * 1024,
    }

    def run(self):
        return self.read() if self.path.is_file() else self.create()

    def read(self):
        with self.path.open("r", encoding="utf-8") as f:
            return load(f)

    def create(self):
        with self.path.open("w", encoding="utf-8") as f:
            dump(self.default, f, indent=2)
            return self.default

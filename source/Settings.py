from json import dump
from json import load
from pathlib import Path

__all__ = ['Settings', 'Batch']


class Settings:
    file = Path(__file__).resolve().parent.parent.joinpath("./settings.json")
    default = {
        "path": "./",
        "folder": "Download",
        "cookie": "",
        "proxies": None,
        "timeout": 10,
        "chunk": 256 * 1024,
    }

    def run(self):
        return self.read() if self.file.is_file() else self.create()

    def read(self):
        with self.file.open("r", encoding="utf-8") as f:
            return load(f)

    def create(self):
        with self.file.open("w", encoding="utf-8") as f:
            dump(self.default, f, indent=2)
            return self.default


class Batch:
    file = Path("./xhs.txt")

    def read_txt(self) -> list:
        if self.file.is_file():
            with self.file.open("r") as f:
                return [i.rstrip('\n') for i in f.readlines()]
        return []

from json import dump
from json import load
from pathlib import Path
from platform import system

__all__ = ['Settings']


class Settings:
    default = {
        "path": "",
        "folder_name": "Download",
        "user_agent": "",
        "cookie": "",
        "proxy": None,
        "timeout": 10,
        "chunk": 1024 * 1024,
        "max_retry": 5,
        "record_data": False,
        "image_format": "webp",
        "video_format": "mp4",
        "folder_mode": False,
    }
    encode = "utf-8-sig"

    def __init__(self, root: Path):
        self.file = root.joinpath("./settings.json")

    def run(self):
        return self.read() if self.file.is_file() else self.create()

    def read(self) -> dict:
        with self.file.open("r", encoding=self.encode) as f:
            return load(f)

    def create(self) -> dict:
        with self.file.open("w", encoding=self.encode) as f:
            dump(self.default, f, indent=4)
            return self.default

    def update(self, data: dict):
        with self.file.open("w", encoding=self.encode) as f:
            dump(data, f, indent=4, ensure_ascii=False)

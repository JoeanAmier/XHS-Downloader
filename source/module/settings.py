from json import dump
from json import load
from pathlib import Path
from platform import system

__all__ = ['Settings']


class Settings:
    default = {
        "work_path": "",
        "folder_name": "Download",
        "user_agent": "",
        "cookie": "",
        "proxy": None,
        "timeout": 10,
        "chunk": 1024 * 1024,
        "max_retry": 5,
        "record_data": False,
        "image_format": "PNG",
        "image_download": True,
        "video_download": True,
        "folder_mode": False,
        "language": "zh_CN",
        "server": False,
    }
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"

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

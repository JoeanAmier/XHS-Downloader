from json import dump, load
from pathlib import Path
from platform import system

from .static import ROOT, USERAGENT

__all__ = ["Settings"]


class Settings:
    default = {
        "mapping_data": {},
        "work_path": "",
        "folder_name": "Download",
        "name_format": "发布时间 作者昵称 作品标题",
        "user_agent": USERAGENT,
        "cookie": "",
        "proxy": None,
        "timeout": 10,
        "chunk": 1024 * 1024 * 2,
        "max_retry": 5,
        "record_data": False,
        "image_format": "PNG",
        "image_download": True,
        "video_download": True,
        "live_download": False,
        "folder_mode": False,
        "download_record": True,
        "author_archive": False,
        "write_mtime": False,
        "markdown_record": False,
        "language": "zh_CN",
    }
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"

    def __init__(self, root: Path = ROOT):
        self.file = root.joinpath("./settings.json")

    def run(self):
        if self.file.is_file():
            data = self.read()
            # 确保所有默认键都存在，提供向后兼容性
            for key, value in self.default.items():
                if key not in data:
                    data[key] = value
            return data
        else:
            return self.create()

    def read(self) -> dict:
        with self.file.open("r", encoding=self.encode) as f:
            return load(f)

    def create(self) -> dict:
        with self.file.open("w", encoding=self.encode) as f:
            dump(self.default, f, indent=4, ensure_ascii=False)
            return self.default

    def update(self, data: dict):
        with self.file.open("w", encoding=self.encode) as f:
            dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def check_keys(
        cls,
        data: dict,
        callback: callable,
        *args,
        **kwargs,
    ) -> dict:
        needful_keys = set(cls.default.keys())
        given_keys = set(data.keys())
        if not needful_keys.issubset(given_keys):
            callback(*args, **kwargs)
            return cls.default
        return data

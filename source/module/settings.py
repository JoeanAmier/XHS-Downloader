from json import dump
from json import load
from pathlib import Path
from platform import system

from .static import ROOT
from .static import SEC_CH_UA
from .static import SEC_CH_UA_PLATFORM
from .static import USERAGENT
import os


__all__ = ['Settings']


class Settings:
    default = {
        "work_path": "",
        "folder_name": "Download",
        "name_format": "发布时间 作者昵称 作品标题",
        "sec_ch_ua": SEC_CH_UA,
        "sec_ch_ua_platform": SEC_CH_UA_PLATFORM,
        "user_agent": USERAGENT,
        "coocie":"abRequestId=f2d143b5-5eb1-5c9c-a5ab-fcd5cbd26c53; a1=18f4de65613ny7qx4bkj74f6em49es001sh5ueoqv30000108214; webId=c4b7153a3b55879c50482f356572aa7c; gid=yYi4fdK2SdyYyYi4fdK2KMdlyqIvWAC4DTVWxAh4iKd642q8jdM887888y8YJy48JWjfWY4J; web_session=040069724a4b7cb60faf1d94b6344b963f46f3; xsecappid=xhs-pc-web; webBuild=4.24.2; acw_tc=4c81bee667bed2e9747c904e76eb0fe3b68e9b779ab1ae4d814056ad87ec25f7; unread={%22ub%22:%22668a06eb0000000005006aba%22%2C%22ue%22:%226671854f000000001c020532%22%2C%22uc%22:17}; websectiga=8886be45f388a1ee7bf611a69f3e174cae48f1ea02c0f8ec3256031b8be9c7ee; sec_poison_id=8903079c-0ac3-4a56-b7e8-b984a4457bad",
        "proxy": None,
        "timeout": 10,
        "chunk": 1024 * 1024,
        "max_retry": 5,
        "record_data": False,
        "image_format": "PNG",
        "image_download": True,
        "video_download": True,
        "live_download": False,
        "folder_mode": False,
        "language": "zh_CN",
        # "server": False,
    }
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"

    def __init__(self, root: Path = ROOT):
        self.file = root.joinpath("./settings.json")
    def run(self):
        return self.read() if self.file.is_file() else self.create()

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

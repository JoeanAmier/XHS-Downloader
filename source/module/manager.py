from pathlib import Path
from re import compile
from re import sub
from shutil import move
from shutil import rmtree
from typing import Callable

from aiohttp import ClientSession
from aiohttp import ClientTimeout

from .static import HEADERS
from .static import USERAGENT

__all__ = ["Manager"]


class Manager:
    NAME = compile(r"[^\u4e00-\u9fffa-zA-Z0-9！？，。；：“”（）《》]")

    def __init__(
            self,
            root: Path,
            path: str,
            folder: str,
            user_agent: str,
            chunk: int,
            cookie: str,
            proxy: str,
            timeout: int,
            retry: int,
            record_data: bool,
            image_format: str,
            image_download: bool,
            video_download: bool,
            folder_mode: bool,
            transition: Callable[[str], str],
    ):
        self.root = root
        self.temp = root.joinpath("./temp")
        self.path = self.__check_path(path)
        self.folder = self.__check_folder(folder)
        self.blank_headers = HEADERS | {
            "User-Agent": user_agent or USERAGENT, }
        self.headers = self.blank_headers | {"Cookie": cookie}
        self.retry = retry
        self.chunk = chunk
        self.record_data = self.check_bool(record_data, False)
        self.image_format = self.__check_image_format(image_format)
        self.folder_mode = self.check_bool(folder_mode, False)
        self.proxy = proxy
        self.request_session = ClientSession(
            headers=self.headers | {
                "Referer": "https://www.xiaohongshu.com/explore", },
            timeout=ClientTimeout(connect=timeout),
        )
        self.download_session = ClientSession(
            headers=self.blank_headers,
            timeout=ClientTimeout(connect=timeout))
        self.message = transition
        self.image_download = self.check_bool(image_download, True)
        self.video_download = self.check_bool(video_download, True)

    def __check_path(self, path: str) -> Path:
        if not path:
            return self.root
        if (r := Path(path)).is_dir():
            return r
        return r if (r := self.__check_root_again(r)) else self.root

    def __check_folder(self, folder: str) -> Path:
        folder = self.path.joinpath(folder or "Download")
        folder.mkdir(exist_ok=True)
        self.temp.mkdir(exist_ok=True)
        return folder

    @staticmethod
    def __check_root_again(root: Path) -> bool | Path:
        if root.resolve().parent.is_dir():
            root.mkdir()
            return root
        return False

    @staticmethod
    def __check_image_format(image_format) -> str:
        if image_format in {"png", "PNG", "webp", "WEBP"}:
            return image_format.lower()
        return "png"

    @staticmethod
    def is_exists(path: Path) -> bool:
        return path.exists()

    @staticmethod
    def delete(path: Path):
        if path.exists():
            path.unlink()

    @staticmethod
    def archive(root: Path, name: str, folder_mode: bool) -> Path:
        return root.joinpath(name) if folder_mode else root

    @staticmethod
    def move(temp: Path, path: Path):
        move(temp.resolve(), path.resolve())

    def __clean(self):
        rmtree(self.temp.resolve())

    def filter_name(self, name: str) -> str:
        name = self.NAME.sub("_", name)
        return sub(r"_+", "_", name).strip("_")

    @staticmethod
    def check_bool(value: bool, default: bool) -> bool:
        return value if isinstance(value, bool) else default

    async def close(self):
        await self.request_session.close()
        await self.download_session.close()
        self.__clean()

from datetime import datetime
from json import dumps
from pathlib import Path
from re import compile
from re import sub
from shutil import move
from shutil import rmtree

from aiohttp import ClientSession
from aiohttp import ClientTimeout

from source.translator import Chinese
from source.translator import English
from .static import COOKIE
from .static import HEADERS
from .static import USERAGENT

__all__ = ["Manager"]


class Manager:
    NAME = compile(r"[^\u4e00-\u9fa5a-zA-Z0-9_]")

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
            folder_mode: bool,
            language: Chinese | English,
    ):
        self.root = root
        self.temp = root.joinpath("./temp")
        self.path = self.__check_path(path)
        self.folder = self.__check_folder(folder)
        self.blank_headers = HEADERS | {
            "User-Agent": user_agent or USERAGENT, }
        self.headers = self.blank_headers | {"Cookie": cookie or COOKIE}
        self.retry = retry
        self.chunk = chunk
        self.record_data = record_data
        self.image_format = self.__check_image_format(image_format)
        self.folder_mode = folder_mode
        self.proxy = proxy
        self.request_session = ClientSession(
            headers=self.headers | {
                "Referer": "https://www.xiaohongshu.com/explore", },
            timeout=ClientTimeout(connect=timeout),
        )
        self.download_session = ClientSession(
            headers=self.blank_headers,
            timeout=ClientTimeout(connect=timeout))
        self.prompt = language

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

    def save_data(self, path: Path, name: str, data: dict):
        if not self.record_data:
            return
        with path.joinpath(f"{name}.txt").open("a", encoding="utf-8") as f:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = f"{
            time.center(
                50,
                "=")}\n{
            dumps(
                data,
                indent=4,
                ensure_ascii=False)}\n"
            f.write(content)

    async def close(self):
        await self.request_session.close()
        await self.download_session.close()
        self.__clean()

from pathlib import Path

from aiohttp import ClientOSError
from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import ServerDisconnectedError
from aiohttp import ServerTimeoutError
from rich.text import Text

from .Html import retry as re_download
from .Static import ERROR, INFO

__all__ = ['Download']


class Download:

    def __init__(self, manager, ):
        self.manager = manager
        self.folder = manager.folder
        self.temp = manager.temp
        self.proxy = manager.proxy
        self.chunk = manager.chunk
        self.session = ClientSession(
            headers={"User-Agent": manager.headers["User-Agent"]},
            timeout=ClientTimeout(connect=manager.timeout))
        self.retry = manager.retry
        self.folder_mode = manager.folder_mode
        self.video_format = manager.video_format
        self.image_format = manager.image_format

    async def run(self, urls: list, name: str, type_: str, log, bar):
        path = self.__generate_path(name)
        if type_ == "v":
            await self.__download(urls[0], path, f"{name}", self.video_format, log, bar)
        elif type_ == "n":
            for index, url in enumerate(urls, start=1):
                await self.__download(url, path, f"{name}_{index}", self.image_format, log, bar)
        else:
            raise ValueError

    def __generate_path(self, name: str):
        path = self.manager.archive(self.folder, name, self.folder_mode)
        path.mkdir(exist_ok=True)
        return path

    @re_download
    async def __download(self, url: str, path: Path, name: str, format_: str, log, bar):
        try:
            async with self.session.get(url, proxy=self.proxy) as response:
                suffix = self.__extract_type(
                    response.headers.get("Content-Type", "")) or format_
                temp = self.temp.joinpath(name)
                file = path.joinpath(name).with_suffix(f".{suffix}")
                if self.manager.is_exists(file):
                    self.rich_log(log, f"{name} 已存在，跳过下载！")
                    return True
                # self.__create_progress(
                #     bar, int(
                #         response.headers.get(
                #             'content-length', 0)) or None)
                with temp.open("wb") as f:
                    async for chunk in response.content.iter_chunked(self.chunk):
                        f.write(chunk)
                        # self.__update_progress(bar, len(chunk))
            self.manager.move(temp, file)
            # self.__create_progress(bar, None)
            self.rich_log(log, f"{name} 下载成功！")
            return True
        except (
                ServerTimeoutError,
                ServerDisconnectedError,
                ClientOSError,
        ):
            self.manager.delete(temp)
            # self.__create_progress(bar, None)
            self.rich_log(log, f"{name} 下载失败！", ERROR)
            return False

    @staticmethod
    def __create_progress(bar, total: int | None):
        if bar:
            bar.update(total=total)

    @staticmethod
    def __update_progress(bar, advance: int):
        if bar:
            bar.advance(advance)

    @staticmethod
    def __extract_type(content: str) -> str:
        return "" if content == "application/octet-stream" else content.split(
            "/")[-1]

    @staticmethod
    def rich_log(log, text, style=INFO):
        if log:
            log.write(Text(text, style=style))
        else:
            print(Text(text, style=style))

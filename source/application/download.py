from asyncio import Semaphore
from asyncio import gather
from pathlib import Path
from typing import TYPE_CHECKING, Any

from aiofiles import open
from httpx import HTTPError

from ..module import ERROR
from ..module import (
    FILE_SIGNATURES_LENGTH,
    FILE_SIGNATURES,
)
from ..module import MAX_WORKERS
# from ..module import WARNING
from ..module import Manager
from ..module import logging
from ..module import retry as re_download
from ..module import sleep_time

if TYPE_CHECKING:
    from httpx import AsyncClient

__all__ = ['Download']


class Download:
    SEMAPHORE = Semaphore(MAX_WORKERS)
    CONTENT_TYPE_MAP = {
        "image/png": "png",
        "image/jpeg": "jpeg",
        "image/webp": "webp",
        "application/octet-stream": "",
        "video/mp4": "mp4",
        "video/quicktime": "mov",
    }

    def __init__(self, manager: Manager, ):
        self.manager = manager
        self.folder = manager.folder
        self.temp = manager.temp
        self.chunk = manager.chunk
        self.client: "AsyncClient" = manager.download_client
        self.headers = manager.blank_headers
        self.retry = manager.retry
        self.message = manager.message
        self.folder_mode = manager.folder_mode
        self.video_format = "mp4"
        self.live_format = "mp4"
        self.image_format = manager.image_format
        self.image_format_list = (
            "jpeg",
            "png",
            "webp",
            "avif",
            "heic",
        )
        self.image_download = manager.image_download
        self.video_download = manager.video_download
        self.live_download = manager.live_download

    async def run(
            self,
            urls: list,
            lives: list,
            index: list | tuple | None,
            name: str,
            type_: str,
            log,
            bar,
    ) -> tuple[Path, list[Any]]:
        path = self.__generate_path(name)
        match type_:
            case "视频":
                tasks = self.__ready_download_video(urls, path, name, log)
            case "图文":
                tasks = self.__ready_download_image(
                    urls, lives, index, path, name, log)
            case _:
                raise ValueError
        tasks = [
            self.__download(
                url,
                path,
                name,
                format_,
                log,
                bar,
            ) for url, name, format_ in tasks
        ]
        tasks = await gather(*tasks)
        return path, tasks

    def __generate_path(self, name: str):
        path = self.manager.archive(self.folder, name, self.folder_mode)
        path.mkdir(exist_ok=True)
        return path

    def __ready_download_video(
            self,
            urls: list[str],
            path: Path,
            name: str,
            log) -> list:
        if not self.video_download:
            logging(log, self.message("视频作品下载功能已关闭，跳过下载"))
            return []
        if self.__check_exists_path(path, f"{name}.{self.video_format}", log):
            return []
        return [(urls[0], name, self.video_format)]

    def __ready_download_image(
            self,
            urls: list[str],
            lives: list[str],
            index: list | tuple | None,
            path: Path,
            name: str,
            log) -> list:
        tasks = []
        if not self.image_download:
            logging(log, self.message("图文作品下载功能已关闭，跳过下载"))
            return tasks
        for i, j in enumerate(zip(urls, lives), start=1):
            if index and i not in index:
                continue
            file = f"{name}_{i}"
            if not any(
                    self.__check_exists_path(
                        path,
                        f"{file}.{s}",
                        log,
                    )
                    for s in self.image_format_list
            ):
                tasks.append([j[0], file, self.image_format])
            if not self.live_download or not j[1] or self.__check_exists_path(
                    path,
                    f"{file}.{self.live_format}",
                    log,
            ):
                continue
            tasks.append([j[1], file, self.live_format])
        return tasks

    def __check_exists_glob(self, path: Path, name: str, log, ) -> bool:
        if any(path.glob(name)):
            logging(
                log, self.message(
                    "{0} 文件已存在，跳过下载").format(name))
            return True
        return False

    def __check_exists_path(self, path: Path, name: str, log, ) -> bool:
        if path.joinpath(name).exists():
            logging(
                log, self.message(
                    "{0} 文件已存在，跳过下载").format(name))
            return True
        return False

    @re_download
    async def __download(
            self,
            url: str,
            path: Path,
            name: str,
            format_: str,
            log,
            bar,
    ):
        async with self.SEMAPHORE:
            headers = self.headers.copy()
            # try:
            #     length, suffix = await self.__head_file(
            #         url,
            #         headers,
            #         format_,
            #     )
            # except HTTPError as error:
            #     logging(
            #         log,
            #         self.message(
            #             "网络异常，{0} 请求失败，错误信息: {1}").format(name, repr(error)),
            #         ERROR,
            #     )
            #     # logging(
            #     #     log,
            #     #     f"{url} Head Headers: {headers.get("Range")}",
            #     #     WARNING,
            #     # )
            #     return False
            # temp = self.temp.joinpath(f"{name}.{suffix}")
            temp = self.temp.joinpath(f"{name}.{format_}")
            self.__update_headers_range(headers, temp, )
            try:
                async with self.client.stream("GET", url, headers=headers, ) as response:
                    await sleep_time()
                    response.raise_for_status()
                    # self.__create_progress(
                    #     bar,
                    #     int(
                    #         response.headers.get(
                    #             'content-length', 0)) or None,
                    # )
                    async with open(temp, "ab") as f:
                        async for chunk in response.aiter_bytes(self.chunk):
                            await f.write(chunk)
                            # self.__update_progress(bar, len(chunk))
                real = await self.__suffix_with_file(
                    temp,
                    path,
                    name,
                    # suffix,
                    format_,
                    log,
                )
                self.manager.move(temp, real)
                # self.__create_progress(bar, None)
                logging(log, self.message("文件 {0} 下载成功").format(real.name))
                return True
            except HTTPError as error:
                # self.manager.delete(temp)
                # self.__create_progress(bar, None)
                logging(
                    log,
                    self.message(
                        "网络异常，{0} 下载失败，错误信息: {1}").format(name, repr(error)),
                    ERROR,
                )
                # logging(
                #     log,
                #     f"{url} Stream Headers: {headers.get("Range")}",
                #     WARNING,
                # )
                return False

    @staticmethod
    def __create_progress(bar, total: int | None, completed=0, ):
        if bar:
            bar.update(total=total, completed=completed)

    @staticmethod
    def __update_progress(bar, advance: int):
        if bar:
            bar.advance(advance)

    @classmethod
    def __extract_type(cls, content: str) -> str:
        return cls.CONTENT_TYPE_MAP.get(content, "")

    async def __head_file(
            self,
            url: str,
            headers: dict[str, str],
            suffix: str,
            # sleep_args: tuple[int, int],
    ) -> tuple[int, str]:
        response = await self.client.head(
            url,
            headers=headers,
        )
        await sleep_time()
        response.raise_for_status()
        suffix = self.__extract_type(
            response.headers.get("Content-Type")) or suffix
        length = response.headers.get(
            "Content-Length", 0)
        return int(length), suffix

    @staticmethod
    def __get_resume_byte_position(file: Path) -> int:
        return file.stat().st_size if file.is_file() else 0

    def __update_headers_range(
            self,
            headers: dict[str, str],
            file: Path,
    ) -> int:
        headers["Range"] = f"bytes={(p := self.__get_resume_byte_position(file))}-"
        return p

    async def __suffix_with_file(
            self,
            temp: Path,
            path: Path,
            name: str,
            default_suffix: str,
            log,
    ) -> Path:
        try:
            async with open(temp, "rb") as f:
                file_start = await f.read(FILE_SIGNATURES_LENGTH)
            for offset, signature, suffix in FILE_SIGNATURES:
                if file_start[offset:offset + len(signature)] == signature:
                    return path.joinpath(f"{name}.{suffix}")
        except Exception as error:
            logging(
                log,
                self.message("文件 {0} 格式判断失败，错误信息：{1}").format(temp.name, repr(error)),
                ERROR,
            )
        return path.joinpath(f"{name}.{default_suffix}")

from asyncio import gather
from pathlib import Path

from httpx import HTTPError

from source.module import ERROR
from source.module import Manager
from source.module import logging
from source.module import retry as re_download

__all__ = ['Download']


class Download:
    CONTENT_TYPE_MAP = {
        "image/png": "png",
        "image/jpeg": "jpg",
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
        self.client = manager.download_client
        self.retry = manager.retry
        self.message = manager.message
        self.folder_mode = manager.folder_mode
        self.video_format = "mp4"
        self.live_format = "mp4"
        self.image_format = manager.image_format
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
    ) -> tuple[Path, tuple]:
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
                bar) for url,
            name,
            format_ in tasks]
        result = await gather(*tasks)
        return path, result

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
        if self.__check_exists(path, f"{name}.{self.video_format}", log):
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
            if not self.__check_exists(
                    path, f"{file}.{self.image_format}", log):
                tasks.append([j[0], file, self.image_format])
            if not self.live_download or not j[1] or self.__check_exists(
                    path, f"{file}.{self.live_format}", log):
                continue
            tasks.append([j[1], file, self.live_format])
        return tasks

    def __check_exists(self, path: Path, name: str, log, ) -> bool:
        if any(path.glob(name)):
            logging(
                log, self.message(
                    "{0} 文件已存在，跳过下载").format(name))
            return True
        return False

    @re_download
    async def __download(self, url: str, path: Path, name: str, format_: str, log, bar):
        temp = self.temp.joinpath(f"{name}.{format_}")
        try:
            async with self.client.stream("GET", url, ) as response:
                response.raise_for_status()
                suffix = self.__extract_type(
                    response.headers.get("Content-Type")) or format_
                real = path.joinpath(f"{name}.{suffix}")
                # self.__create_progress(
                #     bar, int(
                #         response.headers.get(
                #             'content-length', 0)) or None)
                with temp.open("wb") as f:
                    async for chunk in response.aiter_bytes(self.chunk):
                        f.write(chunk)
                        # self.__update_progress(bar, len(chunk))
            self.manager.move(temp, real)
            # self.__create_progress(bar, None)
            logging(log, self.message("文件 {0} 下载成功").format(real.name))
            return True
        except HTTPError as error:
            self.manager.delete(temp)
            # self.__create_progress(bar, None)
            logging(log, str(error), ERROR)
            logging(
                log, self.message(
                    "网络异常，{0} 下载失败").format(name), ERROR)
            return False

    @staticmethod
    def __create_progress(bar, total: int | None):
        if bar:
            bar.update(total=total)

    @staticmethod
    def __update_progress(bar, advance: int):
        if bar:
            bar.advance(advance)

    @classmethod
    def __extract_type(cls, content: str) -> str:
        return cls.CONTENT_TYPE_MAP.get(content, "")

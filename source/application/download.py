from asyncio import gather
from pathlib import Path

from aiohttp import ClientError

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
        "video/quicktime": "mov",
    }

    def __init__(self, manager: Manager, ):
        self.manager = manager
        self.folder = manager.folder
        self.temp = manager.temp
        self.proxy = manager.proxy
        self.chunk = manager.chunk
        self.session = manager.download_session
        self.retry = manager.retry
        self.prompt = manager.prompt
        self.folder_mode = manager.folder_mode
        self.video_format = "mp4"
        self.image_format = manager.image_format

    async def run(self, urls: list, name: str, type_: str, log, bar) -> tuple[Path, tuple]:
        path = self.__generate_path(name)
        match type_:
            case "视频":
                tasks = self.__ready_download_video(urls, path, name, log)
            case "图文":
                tasks = self.__ready_download_image(urls, path, name, log)
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
        if any(path.glob(f"{name}.*")):
            logging(log, self.prompt.skip_download(name))
            return []
        return [(urls[0], name, self.video_format)]

    def __ready_download_image(
            self,
            urls: list[str],
            path: Path,
            name: str,
            log) -> list:
        tasks = []
        for i, j in enumerate(urls, start=1):
            file = f"{name}_{i}"
            if any(path.glob(f"{file}.*")):
                logging(log, self.prompt.skip_download(file))
                continue
            tasks.append([j, file, self.image_format])
        return tasks

    @re_download
    async def __download(self, url: str, path: Path, name: str, format_: str, log, bar):
        try:
            async with self.session.get(url, proxy=self.proxy) as response:
                if response.status != 200:
                    return False
                suffix = self.__extract_type(
                    response.headers.get("Content-Type")) or format_
                temp = self.temp.joinpath(name)
                real = path.joinpath(f"{name}.{suffix}")
                # self.__create_progress(
                #     bar, int(
                #         response.headers.get(
                #             'content-length', 0)) or None)
                with temp.open("wb") as f:
                    async for chunk in response.content.iter_chunked(self.chunk):
                        f.write(chunk)
                        # self.__update_progress(bar, len(chunk))
            self.manager.move(temp, real)
            # self.__create_progress(bar, None)
            logging(log, self.prompt.download_success(name))
            return True
        except ClientError as error:
            self.manager.delete(temp)
            # self.__create_progress(bar, None)
            logging(log, str(error), ERROR)
            logging(log, self.prompt.download_error(name), ERROR)
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

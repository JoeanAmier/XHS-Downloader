from asyncio import Semaphore, gather, sleep
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from aiofiles import open
from curl_cffi.requests.exceptions import RequestException

from ..expansion import CacheError

# from ..module import WARNING
from ..module import (
    ERROR,
    FILE_SIGNATURES,
    FILE_SIGNATURES_LENGTH,
    MAX_WORKERS,
    logging,
    # sleep_time,
)
from ..module import retry as re_download
from ..translation import _

if TYPE_CHECKING:
    from curl_cffi.requests import AsyncSession

    from ..module import Manager

__all__ = ["Download"]


class Download:
    SEMAPHORE = Semaphore(MAX_WORKERS)
    WRITE_BUFFER_SIZE = 1024 * 1024 * 100
    CONTENT_TYPE_MAP = {
        "image/png": "png",
        "image/jpeg": "jpeg",
        "image/webp": "webp",
        "video/mp4": "mp4",
        "video/quicktime": "mov",
        "audio/mp4": "m4a",
        "audio/mpeg": "mp3",
    }

    def __init__(
        self,
        manager: "Manager",
    ):
        self.manager = manager
        self.print = manager.print
        self.folder = manager.folder
        self.temp = manager.temp
        self.chunk = manager.chunk
        self.client: "AsyncSession" = manager.download_client
        self.headers = manager.blank_headers
        self.retry = manager.retry
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
        self.author_archive = manager.author_archive
        self.write_mtime = manager.write_mtime
        # 每个文件下载完成后的间隔(秒)，来自程序设置，用于降低风控风险。
        self.file_delay = manager.file_delay

    async def run(
        self,
        urls: list,
        lives: list,
        index: list | tuple | None,
        path: Path,
        filename: str,
        type_: str,
        mtime: int,
        progress: Callable[[dict], None] | None = None,
        task_id: str | None = None,
    ) -> list[Any]:
        if type_ == _("视频"):
            tasks = self.__ready_download_video(
                urls,
                path,
                filename,
            )
        elif type_ in {
            _("图文"),
            _("图集"),
        }:
            tasks = self.__ready_download_image(
                urls,
                lives,
                index,
                path,
                filename,
            )
        else:
            raise ValueError
        if self.file_delay > 0:
            # 需要控制请求节奏：顺序下载每个文件，并在文件之间应用延迟，
            # 确保 file_delay 真正生效（并发下载会令间隔失效）。
            results = []
            for i, (url, name, format_) in enumerate(tasks):
                results.append(
                    await self.__download(
                        url,
                        path,
                        name,
                        format_,
                        mtime,
                        progress,
                        task_id,
                    )
                )
                # 最后一个文件之后不再等待。
                if i < len(tasks) - 1:
                    await sleep(self.manager.jittered_delay(self.file_delay))
            return results
        # 未设置间隔：保持并发下载以提升速度。
        tasks = [
            self.__download(
                url,
                path,
                name,
                format_,
                mtime,
                progress,
                task_id,
            )
            for url, name, format_ in tasks
        ]
        tasks = await gather(*tasks)
        return tasks

    def generate_path(self, nickname: str, filename: str):
        if self.author_archive:
            folder = self.folder.joinpath(nickname)
            folder.mkdir(exist_ok=True)
        else:
            folder = self.folder
        path = self.manager.archive(folder, filename, self.folder_mode)
        path.mkdir(exist_ok=True)
        return path

    def __ready_download_video(
        self,
        urls: list[str],
        path: Path,
        name: str,
    ) -> list:
        if not self.video_download:
            logging(self.print, _("视频作品下载功能已关闭，跳过下载"))
            return []
        if self.__check_exists_path(
            path,
            f"{name}.{self.video_format}",
        ):
            return []
        return [(urls[0], name, self.video_format)]

    def __ready_download_image(
        self,
        urls: list[str],
        lives: list[str],
        index: list | tuple | None,
        path: Path,
        name: str,
    ) -> list:
        tasks = []
        if not self.image_download:
            logging(self.print, _("图文作品下载功能已关闭，跳过下载"))
            return tasks
        for i, j in enumerate(zip(urls, lives), start=1):
            if index and i not in index:
                continue
            file = f"{name}_{i}"
            if not any(
                self.__check_exists_path(
                    path,
                    f"{file}.{s}",
                )
                for s in self.image_format_list
            ):
                tasks.append([j[0], file, self.image_format])
            if (
                not self.live_download
                or not j[1]
                or self.__check_exists_path(
                    path,
                    f"{file}.{self.live_format}",
                )
            ):
                continue
            tasks.append([j[1], file, self.live_format])
        return tasks

    def __check_exists_glob(
        self,
        path: Path,
        name: str,
    ) -> bool:
        if any(path.glob(name)):
            logging(self.print, _("{0} 文件已存在，跳过下载").format(name))
            return True
        return False

    def __check_exists_path(
        self,
        path: Path,
        name: str,
    ) -> bool:
        if path.joinpath(name).exists():
            logging(self.print, _("{0} 文件已存在，跳过下载").format(name))
            return True
        return False

    @re_download
    async def __download(
        self,
        url: str,
        path: Path,
        name: str,
        format_: str,
        mtime: int,
        progress: Callable[[dict], None] | None,
        task_id: str | None,
    ):
        async with self.SEMAPHORE:
            headers = self.headers.copy()
            temp = self.temp.joinpath(f"{name}.{format_}")
            completed = self.__update_headers_range(
                headers,
                temp,
            )

            def report(state: str, total: int | None = None) -> None:
                if progress:
                    progress(
                        {
                            "task_id": task_id,
                            "filename": f"{name}.{format_}",
                            "completed_bytes": completed,
                            "total_bytes": total,
                            "state": state,
                        }
                    )

            try:
                async with self.client.stream(
                    "GET",
                    url,
                    headers=headers,
                ) as response:
                    # await sleep_time()
                    if response.status_code == 416:
                        raise CacheError(
                            _("文件 {0} 缓存异常，重新下载").format(temp.name),
                        )
                    response.raise_for_status()
                    # self.__create_progress(
                    #     bar,
                    #     int(
                    #         response.headers.get(
                    #             'content-length', 0)) or None,
                    # )
                    content_length = int(response.headers.get("content-length", 0) or 0)
                    total = completed + content_length if content_length else None
                    report("downloading", total)
                    buffer = bytearray()
                    async with open(temp, "ab") as f:
                        async for chunk in response.aiter_content(self.chunk):
                            buffer.extend(chunk)
                            if len(buffer) >= self.WRITE_BUFFER_SIZE:
                                await f.write(bytes(buffer))
                                buffer.clear()
                            completed += len(chunk)
                            report("downloading", total)
                        if buffer:
                            await f.write(bytes(buffer))
                real = await self.__suffix_with_file(
                    temp,
                    path,
                    name,
                    # suffix,
                    format_,
                )
                self.manager.move(
                    temp,
                    real,
                    mtime,
                    self.write_mtime,
                )
                report("completed", total)
                logging(self.print, _("文件 {0} 下载成功").format(real.name))
                return True
            except RequestException as error:
                report("failed")
                logging(
                    self.print,
                    _("网络异常，{0} 下载失败，错误信息: {1}").format(
                        name, repr(error)
                    ),
                    ERROR,
                )
                return False
            except CacheError as error:
                report("failed")
                self.manager.delete(temp)
                logging(
                    self.print,
                    str(error),
                    ERROR,
                )
                return False

    @staticmethod
    def __create_progress(
        bar,
        total: int | None,
        completed=0,
    ):
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
    ) -> tuple[int, str]:
        """未使用"""
        response = await self.client.head(
            url,
            headers=headers,
        )
        # await sleep_time()
        response.raise_for_status()
        suffix = self.__extract_type(response.headers.get("Content-Type")) or suffix
        length = response.headers.get("Content-Length", 0)
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
    ) -> Path:
        try:
            async with open(temp, "rb") as f:
                file_start = await f.read(FILE_SIGNATURES_LENGTH)
            for offset, signature, suffix in FILE_SIGNATURES:
                if file_start[offset : offset + len(signature)] == signature:
                    return path.joinpath(f"{name}.{suffix}")
        except Exception as error:
            logging(
                self.print,
                _("文件 {0} 格式判断失败，错误信息：{1}").format(
                    temp.name, repr(error)
                ),
                ERROR,
            )
        return path.joinpath(f"{name}.{default_suffix}")

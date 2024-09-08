from pathlib import Path
from re import compile
from re import sub
from shutil import move
from shutil import rmtree
from typing import Callable

from httpx import AsyncClient
from httpx import HTTPStatusError
from httpx import RequestError
from httpx import TimeoutException
from httpx import get

from source.expansion import remove_empty_directories
from .static import HEADERS
# from .static import SEC_CH_UA
# from .static import SEC_CH_UA_PLATFORM
from .static import USERAGENT
from .static import WARNING
from .tools import logging

__all__ = ["Manager"]


class Manager:
    NAME = compile(r"[^\u4e00-\u9fffa-zA-Z0-9-_！？，。；：“”（）《》]")
    NAME_KEYS = (
        '收藏数量',
        '评论数量',
        '分享数量',
        '点赞数量',
        '作品标签',
        '作品ID',
        '作品标题',
        '作品描述',
        '作品类型',
        '发布时间',
        '最后更新时间',
        '作者昵称',
        '作者ID',
    )
    NO_PROXY = {
        "http://": None,
        "https://": None,
    }
    SEPARATE = "_"
    WEB_ID = r"(?:^|; )webId=[^;]+"
    WEB_SESSION = r"(?:^|; )web_session=[^;]+"

    def __init__(
            self,
            root: Path,
            path: str,
            folder: str,
            name_format: str,
            chunk: int,
            # sec_ch_ua: str,
            # sec_ch_ua_platform: str,
            user_agent: str,
            cookie: str,
            proxy: str | dict,
            timeout: int,
            retry: int,
            record_data: bool,
            image_format: str,
            image_download: bool,
            video_download: bool,
            live_download: bool,
            download_record: bool,
            folder_mode: bool,
            # server: bool,
            transition: Callable[[str], str],
            _print: bool,
    ):
        self.root = root
        self.temp = root.joinpath("./temp")
        self.path = self.__check_path(path)
        self.folder = self.__check_folder(folder)
        self.message = transition
        self.blank_headers = HEADERS | {
            'user-agent': user_agent or USERAGENT,
            # 'sec-ch-ua': sec_ch_ua or SEC_CH_UA,
            # 'sec-ch-ua-platform': sec_ch_ua_platform or SEC_CH_UA_PLATFORM,
        }
        self.headers = self.blank_headers | {
            'cookie': cookie,
        }
        self.retry = retry
        self.chunk = chunk
        self.name_format = self.__check_name_format(name_format)
        self.record_data = self.check_bool(record_data, False)
        self.image_format = self.__check_image_format(image_format)
        self.folder_mode = self.check_bool(folder_mode, False)
        self.download_record = self.check_bool(download_record, True)
        self.proxy_tip = None
        self.proxy = self.__check_proxy(proxy)
        self.print_proxy_tip(_print, )
        self.request_client = AsyncClient(
            headers=self.headers | {
                'referer': 'https://www.xiaohongshu.com/',
            },
            timeout=timeout,
            verify=False,
            follow_redirects=True,
            **self.proxy,
        )
        self.download_client = AsyncClient(
            headers=self.blank_headers,
            timeout=timeout,
            verify=False,
            follow_redirects=True,
            **self.proxy,
        )
        self.image_download = self.check_bool(image_download, True)
        self.video_download = self.check_bool(video_download, True)
        self.live_download = self.check_bool(live_download, True)
        # self.server = self.check_bool(server, False)

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
        await self.request_client.aclose()
        await self.download_client.aclose()
        # self.__clean()
        remove_empty_directories(self.root)
        remove_empty_directories(self.folder)

    def __check_name_format(self, format_: str) -> str:
        keys = format_.split()
        return next(
            (
                "发布时间 作者昵称 作品标题"
                for key in keys
                if key not in self.NAME_KEYS
            ),
            format_,
        )

    def __check_proxy(
            self,
            proxy: str | dict,
            url="https://www.xiaohongshu.com/explore",
    ) -> dict:
        if not proxy:
            return {"proxies": self.NO_PROXY}
        if isinstance(proxy, str):
            kwarg = {"proxy": proxy}
        elif isinstance(proxy, dict):
            kwarg = {"proxies": proxy}
        else:
            self.proxy_tip = (
                self.message("proxy 参数 {0} 设置错误，程序将不会使用代理").format(proxy), WARNING,)
            return {"proxies": self.NO_PROXY}
        try:
            response = get(
                url,
                **kwarg, )
            response.raise_for_status()
            self.proxy_tip = (self.message("代理 {0} 测试成功").format(proxy),)
            return kwarg
        except TimeoutException:
            self.proxy_tip = (
                self.message("代理 {0} 测试超时").format(proxy), WARNING,)
        except (
                RequestError,
                HTTPStatusError,
        ) as e:
            self.proxy_tip = (
                self.message("代理 {0} 测试失败：{1}").format(
                    proxy, e), WARNING,)
        return {"proxies": self.NO_PROXY}

    def print_proxy_tip(self, _print: bool = True, log=None, ) -> None:
        if _print and self.proxy_tip:
            logging(log, *self.proxy_tip)

    @classmethod
    def clean_cookie(cls, cookie_string: str) -> str:
        return cls.delete_cookie(
            cookie_string,
            (
                cls.WEB_ID,
                cls.WEB_SESSION,
            ),
        )

    @classmethod
    def delete_cookie(cls, cookie_string: str, patterns: list | tuple) -> str:
        for pattern in patterns:
            # 使用空字符串替换匹配到的部分
            cookie_string = sub(pattern, "", cookie_string)
        # 去除多余的分号和空格
        cookie_string = sub(r';\s*$', "", cookie_string)  # 删除末尾的分号和空格
        cookie_string = sub(r';\s*;', ";", cookie_string)  # 删除中间多余分号后的空格
        return cookie_string.strip('; ')

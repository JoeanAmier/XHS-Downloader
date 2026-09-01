from http.cookies import SimpleCookie
from os import utime
from pathlib import Path
from re import compile, sub
from shutil import move, rmtree
from typing import TYPE_CHECKING, get_args

from curl_cffi.requests import AsyncSession, BrowserTypeLiteral, get
from curl_cffi.requests.exceptions import RequestException, Timeout

from source.expansion import remove_empty_directories

from ..translation import _
from .static import HEADERS, IMPERSONATE, WARNING
from .tools import get_site_referer, logging

if TYPE_CHECKING:
    from ..expansion import Cleaner

__all__ = ["Manager"]


class Manager:
    NAME = compile(r"[^\u4e00-\u9fffa-zA-Z0-9-_！？，。；：“”（）《》]")
    NAME_KEYS = (
        "收藏数量",
        "评论数量",
        "分享数量",
        "点赞数量",
        "作品标签",
        "作品ID",
        "作品标题",
        "作品描述",
        "作品类型",
        "发布时间",
        "最后更新时间",
        "作者昵称",
        "作者ID",
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
        impersonate: str,
        cookie: str,
        proxy: str | None,
        proxy_download: bool,
        timeout: int,
        retry: int,
        record_data: bool,
        image_format: str,
        image_download: bool,
        video_download: bool,
        live_download: bool,
        video_preference: str,
        download_record: bool,
        folder_mode: bool,
        author_archive: bool,
        write_mtime: bool,
        script_server: bool,
        note_format: str,
        cleaner: "Cleaner",
        print_object,
    ):
        self.print = print_object
        self.root = root
        self.cleaner = cleaner
        self.temp = root.joinpath("Temp")
        self.path = self.__check_path(path)
        self.folder = self.__check_folder(folder)
        self.compatible()
        self.blank_headers = HEADERS.copy()
        self.impersonate = self.__check_impersonate(impersonate)
        self.retry = self.__check_integer(retry, 5, 0)
        self.chunk = self.__check_integer(chunk, 2 * 1024 * 1024, 1024 * 1024)
        self.name_format = self.__check_name_format(name_format)
        self.record_data = self.check_bool(record_data, False)
        self.image_format = self.__check_image_format(image_format)
        self.folder_mode = self.check_bool(folder_mode, False)
        self.download_record = self.check_bool(download_record, True)
        self.timeout = self.__check_integer(timeout, 10, 1)
        self.proxy_tip = None
        self.proxy_download = self.check_bool(proxy_download, False)
        self.proxy = self.__check_proxy(proxy)
        self.print_proxy_tip()
        # 支持多个 Cookie：按换行分隔解析成列表，请求时严格轮流选用，失败时切换到下一个。
        self.cookies = self.__parse_cookies(cookie)
        self.cookie = self.cookies[0] if self.cookies else ""
        # 轮流指针：指向下一次要使用的 Cookie 下标。
        self._cookie_index = 0
        # 单 Cookie 保持原有烘焙行为；多 Cookie 时不烘焙，改为每次请求通过 header 精确指定。
        jar_cookies = (
            self.cookie_str_to_dict(self.cookie) if len(self.cookies) <= 1 else {}
        )
        self.request_client = AsyncSession(
            headers=self.blank_headers,
            cookies=jar_cookies,
            timeout=self.timeout,
            verify=False,
            allow_redirects=True,
            proxy=self.proxy,
            impersonate=self.impersonate,
        )
        self.download_client = AsyncSession(
            timeout=self.timeout,
            verify=False,
            allow_redirects=True,
            proxy=self.proxy if self.proxy_download else None,
            impersonate=self.impersonate,
        )
        self.image_download = self.check_bool(image_download, True)
        self.video_download = self.check_bool(video_download, True)
        self.video_preference = self.check_video_preference(video_preference)
        self.live_download = self.check_bool(live_download, True)
        self.author_archive = self.check_bool(author_archive, False)
        self.write_mtime = self.check_bool(write_mtime, False)
        self.script_server = self.check_bool(script_server, False)
        self.note_format = self.__check_note_format(note_format)
        self.create_folder()

    def __check_path(self, path: str) -> Path:
        if not path:
            return self.root
        if (r := Path(path)).is_dir():
            return r
        return r if (r := self.__check_root_again(r)) else self.root

    def __check_folder(self, folder: str) -> Path:
        folder = self.cleaner.filter_name(folder, default="Download")
        return self.path.joinpath(folder)

    @staticmethod
    def __check_root_again(root: Path) -> None | Path:
        if root.parent.is_dir():
            root.mkdir(exist_ok=True)
            return root
        return None

    @staticmethod
    def __check_image_format(image_format) -> str:
        if (i := image_format.lower()) in {
            "auto",
            "png",
            "webp",
            "jpeg",
            "heic",
            "avif",
        }:
            return i
        return "jpeg"

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

    @classmethod
    def move(
        cls,
        temp: Path,
        path: Path,
        mtime: int = None,
        rewrite: bool = False,
    ):
        move(temp.resolve(), path.resolve())
        if rewrite and mtime:
            cls.update_mtime(path.resolve(), mtime)

    @staticmethod
    def update_mtime(file: Path, mtime: int):
        utime(file, (mtime, mtime))

    def __clean(self):
        rmtree(self.temp.resolve())

    def filter_name(self, name: str) -> str:
        name = self.NAME.sub("_", name)
        return sub(r"_+", "_", name).strip("_")

    @staticmethod
    def check_bool(value: bool, default: bool) -> bool:
        return value if isinstance(value, bool) else default

    @staticmethod
    def __check_integer(value: int, default: int, minimum: int) -> int:
        """将配置中的整数参数限制在下载器可接受的范围内。"""

        try:
            return max(minimum, value)
        except (TypeError, ValueError):
            return default

    async def close(self):
        await self.request_client.close()
        await self.download_client.close()
        # self.__clean()
        remove_empty_directories(self.root)
        remove_empty_directories(self.folder)

    def __check_name_format(self, format_: str) -> str:
        keys = format_.split()
        return next(
            ("发布时间 作者昵称 作品标题" for key in keys if key not in self.NAME_KEYS),
            format_,
        )

    @staticmethod
    def check_video_preference(preference: str) -> str:
        if preference in {"resolution", "bitrate", "size"}:
            return preference
        return "resolution"

    @staticmethod
    def __check_note_format(note_format: str) -> str:
        if note_format in {"txt", "md", "all"}:
            return note_format
        return ""

    def __check_proxy(
        self,
        proxy: str | None,
        url="https://www.xiaohongshu.com/explore",
    ) -> str | None:
        if proxy:
            try:
                response = get(
                    url,
                    timeout=self.timeout,
                    impersonate=self.impersonate,
                    proxy=proxy,
                )
                response.raise_for_status()
                self.proxy_tip = (_("代理 {0} 测试成功").format(proxy),)
                return proxy
            except Timeout:
                self.proxy_tip = (
                    _("代理 {0} 测试超时").format(proxy),
                    WARNING,
                )
            except RequestException as e:
                self.proxy_tip = (
                    _("代理 {0} 测试失败：{1}").format(
                        proxy,
                        e,
                    ),
                    WARNING,
                )
        return None

    def get_headers(
        self,
        url: str = "",
    ) -> dict:
        headers = self.blank_headers.copy()
        headers["referer"] = get_site_referer(url)
        return headers

    def __check_impersonate(self, impersonate: str) -> str:
        if impersonate in get_args(BrowserTypeLiteral):
            return impersonate
        logging(
            self.print,
            _("impersonate 参数错误，使用默认值: {0}").format(IMPERSONATE),
            WARNING,
        )
        return IMPERSONATE

    def print_proxy_tip(
        self,
    ) -> None:
        if self.proxy_tip:
            logging(self.print, *self.proxy_tip)

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
        cookie_string = sub(r";\s*$", "", cookie_string)  # 删除末尾的分号和空格
        cookie_string = sub(r";\s*;", ";", cookie_string)  # 删除中间多余分号后的空格
        return cookie_string.strip("; ")

    def create_folder(
        self,
    ):
        self.folder.mkdir(exist_ok=True)
        self.temp.mkdir(exist_ok=True)

    def compatible(
        self,
    ):
        if (
            self.path == self.root
            and (old := self.path.parent.joinpath(self.folder.name)).exists()
            and not self.folder.exists()
        ):
            move(old, self.folder)

    @staticmethod
    def cookie_str_to_dict(cookie_str: str) -> dict:
        cookie = SimpleCookie()
        cookie.load(cookie_str)
        return {key: morsel.value for key, morsel in cookie.items()}

    @staticmethod
    def __parse_cookies(cookie_str: str) -> list[str]:
        """把配置中的 Cookie 文本按换行拆分为多个有效 Cookie。"""

        if not cookie_str:
            return []
        return [part.strip() for part in cookie_str.splitlines() if part.strip()]

    def pick_cookie(self, exclude: str | None = None) -> str:
        """严格轮流（round-robin）取下一个 Cookie；若正好是上次失败的 exclude，则再跳一个。"""

        if not self.cookies:
            return ""
        if len(self.cookies) == 1:
            return self.cookies[0]
        count = len(self.cookies)
        selected = self.cookies[self._cookie_index % count]
        self._cookie_index = (self._cookie_index + 1) % count
        # 如果选中的正好是上次失败的 Cookie，跳过一个改用下一个。
        if exclude is not None and selected == exclude:
            selected = self.cookies[self._cookie_index % count]
            self._cookie_index = (self._cookie_index + 1) % count
        return selected

    @property
    def cookie_count(self) -> int:
        return len(self.cookies)

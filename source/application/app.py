from re import compile

from source.expansion import Converter
from source.expansion import Namespace
from source.module import Manager
from source.module import (
    ROOT,
    ERROR,
    WARNING,
)
from source.module import logging
from source.translator import (
    LANGUAGE,
    Chinese,
    English,
)
from .Downloader import Download
from .Explore import Explore
from .Html import Html
from .Image import Image
from .Video import Video

__all__ = ["XHS"]


class XHS:
    LINK = compile(r"https?://www\.xiaohongshu\.com/explore/[a-z0-9]+")
    SHARE = compile(r"https?://www\.xiaohongshu\.com/discovery/item/[a-z0-9]+")
    SHORT = compile(r"https?://xhslink\.com/[A-Za-z0-9]+")
    __INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if not cls.__INSTANCE:
            cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE

    def __init__(
            self,
            work_path="",
            folder_name="Download",
            user_agent: str = None,
            cookie: str = None,
            proxy: str = None,
            timeout=10,
            chunk=1024 * 1024,
            max_retry=5,
            record_data=False,
            image_format="PNG",
            folder_mode=False,
            language="zh-CN",
            language_object: Chinese | English = None,
    ):
        self.prompt = language_object or LANGUAGE.get(language, Chinese)
        self.manager = Manager(
            ROOT,
            work_path,
            folder_name,
            user_agent,
            chunk,
            cookie,
            proxy,
            timeout,
            max_retry,
            record_data,
            image_format,
            folder_mode,
            self.prompt,
        )
        self.html = Html(self.manager)
        self.image = Image()
        self.video = Video()
        self.explore = Explore()
        self.convert = Converter()
        self.download = Download(self.manager)

    def __extract_image(self, container: dict, data: Namespace):
        container["下载地址"] = self.image.get_image_link(
            data, self.manager.image_format)

    def __extract_video(self, container: dict, data: Namespace):
        container["下载地址"] = self.video.get_video_link(data)

    async def __download_files(self, container: dict, download: bool, log, bar):
        name = self.__naming_rules(container)
        path = self.manager.folder
        if (u := container["下载地址"]) and download:
            path = await self.download.run(u, name, container["作品类型"], log, bar)
        elif not u:
            logging(log, self.prompt.download_link_error, ERROR)
        self.manager.save_data(path, name, container)

    async def extract(self, url: str, download=False, log=None, bar=None) -> list[dict]:
        # return  # 调试代码
        urls = await self.__extract_links(url, log)
        if not urls:
            logging(log, self.prompt.extract_link_failure, WARNING)
        else:
            logging(log, self.prompt.pending_processing(len(urls)))
        # return urls  # 调试代码
        return [await self.__deal_extract(i, download, log, bar) for i in urls]

    async def __extract_links(self, url: str, log) -> list:
        urls = []
        for i in url.split():
            if u := self.SHORT.search(i):
                i = await self.html.request_url(
                    u.group(), False, log)
            if u := self.SHARE.search(i):
                urls.append(u.group())
            elif u := self.LINK.search(i):
                urls.append(u.group())
        return urls

    async def __deal_extract(self, url: str, download: bool, log, bar):
        logging(log, self.prompt.start_processing(url))
        html = await self.html.request_url(url, log=log)
        # logging(log, html)  # 调试代码
        if not html:
            logging(log, self.prompt.get_data_failure(url), ERROR)
            return {}
        namespace = self.__generate_data_object(html)
        data = self.explore.run(namespace)
        # logging(log, data)  # 调试代码
        if not data:
            logging(log, self.prompt.extract_data_failure(url), ERROR)
            return {}
        match data["作品类型"]:
            case "视频":
                self.__extract_video(data, namespace)
            case "图文":
                self.__extract_image(data, namespace)
            case _:
                data["下载地址"] = []
        await self.__download_files(data, download, log, bar)
        logging(log, self.prompt.processing_completed(url))
        return data

    def __generate_data_object(self, html: str) -> Namespace:
        data = self.convert.run(html)
        return Namespace(data)

    def __naming_rules(self, data: dict) -> str:
        """下载文件默认使用 作品标题 或 作品 ID 作为文件名称，可修改此方法自定义文件名称格式"""
        return self.manager.filter_name(data["作品标题"]) or data["作品ID"]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def close(self):
        await self.manager.close()

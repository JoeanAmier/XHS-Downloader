from re import compile

from .Downloader import Download
from .Explore import Explore
from .Html import Html
from .Image import Image
from .Manager import Manager
from .Static import (
    ROOT,
    ERROR,
    WARNING,
)
from .Video import Video


class XHS:
    LINK = compile(r"https?://www\.xiaohongshu\.com/explore/[a-z0-9]+")
    SHARE = compile(r"https?://www\.xiaohongshu\.com/discovery/item/[a-z0-9]+")
    SHORT = compile(r"https?://xhslink\.com/[A-Za-z0-9]+")
    __INSTANCE = None
    TYPE = {
        "视频": "v",
        "图文": "n",
    }

    def __new__(cls, *args, **kwargs):
        if not cls.__INSTANCE:
            cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE

    def __init__(
            self,
            path="",
            folder_name="Download",
            user_agent: str = None,
            cookie: str = None,
            proxy: str = None,
            timeout=10,
            chunk=1024 * 1024,
            max_retry=5,
            record_data=False,
            image_format="webp",
            video_format="mp4",
            folder_mode=False,
    ):
        self.manager = Manager(
            ROOT,
            path,
            folder_name,
            user_agent,
            chunk,
            cookie,
            proxy,
            timeout,
            max_retry,
            record_data,
            image_format,
            video_format,
            folder_mode,
        )
        self.html = Html(self.manager)
        self.image = Image()
        self.video = Video()
        self.explore = Explore()
        self.download = Download(self.manager, )
        self.rich_log = self.download.rich_log

    def __extract_image(self, container: dict, html: str):
        container["下载地址"] = self.image.get_image_link(html)

    def __extract_video(self, container: dict, html: str):
        container["下载地址"] = self.video.get_video_link(html)

    async def __download_files(self, container: dict, download: bool, log, bar):
        name = self.__naming_rules(container)
        if (u := container["下载地址"]) and download:
            await self.download.run(u, name, self.TYPE[container["作品类型"]], log, bar)
        elif not u:
            self.rich_log(log, "提取作品文件下载地址失败！", ERROR)
        self.manager.save_data(name, container)

    async def extract(self, url: str, download=False, log=None, bar=None) -> list[dict]:
        # return  # 调试代码
        urls = await self.__extract_links(url)
        if not urls:
            self.rich_log(log, "提取小红书作品链接失败！", WARNING)
        else:
            self.rich_log(log, f"共 {len(urls)} 个小红书作品待处理...")
        # return urls  # 调试代码
        return [await self.__deal_extract(i, download, log, bar) for i in urls]

    async def __extract_links(self, url: str) -> list:
        urls = []
        for i in url.split():
            if u := self.SHORT.search(i):
                i = await self.html.request_url(
                    u.group(), False)
            if u := self.SHARE.search(i):
                urls.append(u.group())
            elif u := self.LINK.search(i):
                urls.append(u.group())
        return urls

    async def __deal_extract(self, url: str, download: bool, log, bar):
        self.rich_log(log, f"开始处理作品：{url}")
        html = await self.html.request_url(url)
        # self.rich_log(log, html)  # 调试代码
        if not html:
            self.rich_log(log, f"{url} 获取数据失败！", ERROR)
            return {}
        data = self.explore.run(html)
        # self.rich_log(log, data)  # 调试代码
        if not data:
            self.rich_log(log, f"{url} 提取数据失败！", ERROR)
            return {}
        match data["作品类型"]:
            case "视频":
                self.__extract_video(data, html)
            case "图文":
                self.__extract_image(data, html)
            case _:
                data["下载地址"] = []
        await self.__download_files(data, download, log, bar)
        self.rich_log(log, f"作品处理完成：{url}")
        return data

    def __naming_rules(self, data: dict) -> str:
        """下载文件默认使用 作品标题 或 作品 ID 作为文件名称，可修改此方法自定义文件名称格式"""
        return self.manager.filter_name(data["作品标题"]) or data["作品ID"]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def close(self):
        self.manager.clean()
        await self.html.session.close()
        await self.download.session.close()

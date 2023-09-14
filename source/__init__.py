from pathlib import Path
from re import compile

from .Download import Download
from .Explore import Explore
from .Html import Html
from .Image import Image
from .Settings import Batch
from .Settings import Settings
from .Video import Video

__all__ = ['XHS', 'Settings', 'Batch']


class XHS:
    ROOT = Path(__file__).resolve().parent.parent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Cookie": "abRequestId=27dafe41-28af-5b33-9f22-fe05d8c4ac2f; xsecappid=xhs-pc-web; a1=18a363d90c9gw7eaz2krqhj4c"
                  "x2gtwgotul1wur8950000289463; webId=27fb29ed7ff41eadd4bc58197a465b63; web_session=030037a3d84590608f6"
                  "da85793234a9a6588ed; gid=yY0qKqfd2Y9qyY0qKqfj877FSjkEWd0uJTFA1YjxV4SCJy28k9EklE888JYj4Kq82242dKiY; w"
                  "ebBuild=3.8.1; websectiga=3633fe24d49c7dd0eb923edc8205740f10fdb18b25d424d2a2322c6196d2a4ad; sec_pois"
                  "on_id=179f847f-ba58-4ede-86bf-977d710da3b2; cache_feeds=[]",
    }
    links = compile(r"https://www.xiaohongshu.com/explore/[0-9a-z]+")

    def __init__(
            self,
            path="./",
            folder="Download",
            cookie=None,
            proxies=None,
            timeout=10,
            chunk=256 * 1024,
    ):
        self.__update_cookie(cookie)
        self.html = Html(self.headers, proxies, timeout)
        self.image = Image()
        self.video = Video()
        self.explore = Explore()
        self.download = Download(
            self.ROOT,
            path,
            folder,
            self.headers,
            proxies,
            chunk)

    def __get_image(self, container: dict, html: str, download):
        urls = self.image.get_image_link(html)
        if download:
            self.download.run(urls, self.__naming_rules(container), 1)
        container["下载地址"] = urls

    def __get_video(self, container: dict, html: str, download):
        url = self.video.get_video_link(html)
        if download:
            self.download.run(url, self.__naming_rules(container), 0)
        container["下载地址"] = url

    def extract(self, url: str, download=False) -> dict:
        if not self.__check(url):
            print(f"无效的作品链接: {url}")
            return {}
        html = self.html.get_html(url)
        if not html:
            return {}
        data = self.explore.run(html)
        if not data:
            print(f"获取作品数据失败: {url}")
            return {}
        if data["作品类型"] == "视频":
            self.__get_video(data, html, download)
        else:
            self.__get_image(data, html, download)
        return data

    def __check(self, url: str):
        return self.links.match(url)

    @staticmethod
    def __naming_rules(data: dict) -> str:
        """下载文件默认使用作品 ID 作为文件名，可修改此方法自定义文件名格式"""
        return data["作品ID"]

    def __update_cookie(self, cookie: str) -> None:
        if cookie and isinstance(cookie, str):
            self.headers["Cookie"] = cookie

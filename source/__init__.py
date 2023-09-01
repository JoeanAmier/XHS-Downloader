from re import compile

from .Download import Download
from .Explore import Explore
from .Html import Html
from .Image import Image
from .Settings import Settings
from .Video import Video

__all__ = ['XHS', 'Settings']


class XHS:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }
    links = compile(r"https://www.xiaohongshu.com/explore/[0-9a-z]+")

    def __init__(
            self,
            path="./",
            folder="Download",
            proxies=None,
            timeout=10,
            chunk=256 * 1024,
    ):
        self.html = Html(self.headers, proxies, timeout)
        self.image = Image()
        self.video = Video()
        self.explore = Explore()
        self.download = Download(
            path,
            folder,
            self.headers,
            proxies,
            chunk)

    def __get_image(self, container: dict, html: str, download):
        urls = self.image.get_image_link(html)
        if download:
            self.download.run(urls, self.__naming_rules(container))
        container["下载地址"] = urls

    def __get_video(self, container: dict, html: str, download):
        url = self.video.get_video_link(html)
        if download:
            self.download.run(url, self.__naming_rules(container))
        container["下载地址"] = url

    def extract(self, url: str, download=False) -> dict:
        if not self.__check(url):
            return {}
        html = self.html.get_html(url)
        if not html:
            return {}
        data = self.explore.run(html)
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

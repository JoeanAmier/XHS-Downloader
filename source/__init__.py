from re import compile

from .Download import Download
from .Explore import Explore
from .Html import Html
from .Image import Image
from .Manage import Manager
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
        self.manager = Manager()
        self.image = Image()
        self.video = Video()
        self.explore = Explore()
        self.download = Download(self.manager, path, folder, self.headers, proxies, chunk)

    def get_image(self, container: dict, html: str, download):
        urls = self.image.get_image_link(html)
        if download:
            self.download.run(urls, container["作品ID"])
        container["下载地址"] = urls

    def get_video(self, container: dict, html: str, download):
        url = self.video.get_video_link(html)
        if download:
            self.download.run(url, container["作品ID"])
        container["下载地址"] = url

    def extract(self, url: str, download=False) -> dict:
        if not self.check(url):
            return {}
        html = self.html.get_html(url)
        if not html:
            return {}
        data = self.explore.run(html)
        if data["作品类型"] == "视频":
            self.get_video(data, html, download)
        else:
            self.get_image(data, html, download)
        return data

    def check(self, url: str):
        return self.links.match(url)

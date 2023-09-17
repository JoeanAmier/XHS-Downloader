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
        "Cookie": "abRequestId=0a09e155-fa93-54c9-b164-a1c2d91f0669; webBuild=3.8.2; a1=18aa21f6e2e5dyk1w1r0zbtulnsbc"
                  "5nlhcqklucqb50000310139; webId=f32bd0ca48726f93238c13047e92d891; websectiga=6169c1e84f393779a5f7de"
                  "7303038f3b47a78e47be716e7bec57ccce17d45f99; sec_poison_id=b1c18309-a338-4dc4-9fb1-6fe21b15af09; we"
                  "b_session=030037a235e4642c22125cf67e224a10791e83; gid=yY00JyiSKyxqyY00JyiKdS7SJd2fvTyEyF8uAADD971I"
                  "MT28DS2I11888qy8yqj8Kf04iydj; cache_feeds=[]; xsecappid=xhs-pc-web",
    }
    links = compile(r"https://www.xiaohongshu.com/explore/[0-9a-z]+")

    def __init__(
            self,
            path="",
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

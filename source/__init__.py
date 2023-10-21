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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                      "/116.0.0.0 Safari/537.36",
        "Cookie": "abRequestId=8bf8c305-4e5b-52dd-a723-e9a5343ab42d; webBuild=3.11.3; xsecappid=xhs-pc-web"
                  "; a1=18b5003660f88kld0gicpx2on2oksepl5y3r9htmn50000247235; webId=a2b049d2fa82434385976a4"
                  "9814085b0; websectiga=16f444b9ff5e3d7e258b5f7674489196303a0b160e16647c6c2b4dcb609f4134; s"
                  "ec_poison_id=3d97668d-1e50-42a7-89c0-7b46aa0183a5; web_session=030037a2006067cf0a2b5f724b"
                  "224a1819eb36; gid=yYD288qW4824yYD288qKKvx98iYYT1f8k3SUq6ICJlIJlF28TMdU1j888J4WJq28fqDJiqq"
                  "0; unread={%22ub%22:%22650533d4000000001302862b%22%2C%22ue%22:%2265015857000000001e021a5e"
                  "%22%2C%22uc%22:42}",
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

    def __get_image(self, container: dict, html: str, download, log):
        urls = self.image.get_image_link(html)
        if download:
            self.download.run(urls, self.__naming_rules(container), 1, log)
        container["下载地址"] = urls

    def __get_video(self, container: dict, html: str, download, log):
        url = self.video.get_video_link(html)
        if download:
            self.download.run(url, self.__naming_rules(container), 0, log)
        container["下载地址"] = url

    def extract(self, url: str, download=False, log=None) -> dict:
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
            self.__get_video(data, html, download, log)
        else:
            self.__get_image(data, html, download, log)
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

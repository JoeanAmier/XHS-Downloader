from re import compile

from .Download import Download
from .Explore import Explore
from .Html import Html
from .Image import Image
from .Video import Video


class XHS:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Referer": "https://www.xiaohongshu.com/",
        "Cookie": "abRequestId=27dafe41-28af-5b33-9f22-fe05d8c4ac2f; xsecappid=xhs-pc-web; a1=18a363d90c9gw7eaz2krqhj4cx2gtwgotul1wur8950000289463; webId=27fb29ed7ff41eadd4bc58197a465b63; websectiga=cffd9dcea65962b05ab048ac76962acee933d26157113bb213105a116241fa6c; sec_poison_id=3a1e34ee-3535-4ee9-8186-4d574da5291e; web_session=030037a3d84590608f6da85793234a9a6588ed; gid=yY0qKqfd2Y9qyY0qKqfj877FSjkEWd0uJTFA1YjxV4SCJy28k9EklE888JYj4Kq82242dKiY; webBuild=3.6.0; cache_feeds=[]",
    }
    links = compile(r"https://www.xiaohongshu.com/explore/[0-9a-z]+")

    def __init__(
            self,
            path="./",
            folder="Download",
            headers=None,
            proxies=None,
            timeout=10,
            cookie=None):
        self.set_cookie(cookie)
        self.html = Html(headers or self.headers, proxies, timeout)
        self.image = Image()
        self.video = Video()
        self.explore = Explore()
        self.download = Download(path, folder, self.html.headers, proxies)

    def set_cookie(self, cookie: str):
        if cookie:
            self.headers["Cookie"] = cookie

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

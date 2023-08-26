from .Download import Download
from .Explore import Explore
from .Html import Html
from .Image import Image
from .Video import Video


class XHS:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        "Cookie": "abRequestId=fd245483-beed-57b0-abfc-440b6a6be2aa; webBuild=3.4.1; xsecappid=xhs-pc-web; a1=189fe37918ezx1jqcbe9fin95cnxqj2ewcbc250yp50000234538; webId=9fff21309cfd3e4f380a6c75ed463803; websectiga=f47eda31ec99545da40c2f731f0630efd2b0959e1dd10d5fedac3dce0bd1e04d; sec_poison_id=003395d3-6520-4a02-851a-17d093203251; web_session=030037a3efee2e602d5d16fca4234a8a44466c; gid=yYjidqWi2KE4yYjidqWjyS28YduCyVASDdjiDvU3Ij2SIS28CAVJdJ888Jq42qY88J44DyjS",
    }

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

    def get_image(self, url: str, download=False):
        urls = self.image.get_image_link(url)
        if download:
            self.download.run(urls)
        return urls

    def get_video(self, url: str, download=False):
        url = self.video.get_video_link(url)
        if download:
            self.download.run([url])
        return url

    def extract(self, url: str):
        html = self.html.get_html(url)
        if not html:
            return None
        self.explore.run(html)

from .Html import Html
from .Image import Image
from .Params import Params
from .Video import Video

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
    "Cookie": "abRequestId=fd245483-beed-57b0-abfc-440b6a6be2aa; webBuild=3.4.1; xsecappid=xhs-pc-web; a1=189fe37918ezx1jqcbe9fin95cnxqj2ewcbc250yp50000234538; webId=9fff21309cfd3e4f380a6c75ed463803; websectiga=f47eda31ec99545da40c2f731f0630efd2b0959e1dd10d5fedac3dce0bd1e04d; sec_poison_id=003395d3-6520-4a02-851a-17d093203251; web_session=030037a3efee2e602d5d16fca4234a8a44466c; gid=yYjidqWi2KE4yYjidqWjyS28YduCyVASDdjiDvU3Ij2SIS28CAVJdJ888Jq42qY88J44DyjS",
}


class XHS:
    def __init__(self, path="./", headers=None, proxies=None, timeout=10):
        self.params = Params(path)
        self.html = Html(headers or HEADERS, proxies, timeout)
        self.image = Image(self.html, self.params)
        self.video = Video(self.html, self.params)
        self._cookie = ""

    def get_image(self, url: str, download=False):
        return self.image.get_image_link(url, download)

    def get_video(self, url: str, download=False):
        return self.video.get_video_link(url, download)

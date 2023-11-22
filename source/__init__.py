from pathlib import Path
from re import compile

from textual.app import App
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import HorizontalScroll
from textual.containers import ScrollableContainer
from textual.widgets import Button
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import Log

from .Download import Download
from .Explore import Explore
from .Html import Html
from .Image import Image
from .Settings import Batch
from .Settings import Settings
from .Video import Video

__all__ = ['XHS', 'XHSDownloader']


class XHS:
    ROOT = Path(__file__).resolve().parent.parent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                      "/116.0.0.0 Safari/537.36",
        "Cookie": "abRequestId=c76828f5-4f37-5b3b-8cc3-036eb91b2edb; webBuild=3.14.1; xsecappid=xhs-pc-web; "
                  "a1=18ba9b2b23co9uwihz4adkebwsw05g8upycgsldyj50000141248; webId=23ee7745020025247828cf8d6d0decff; "
                  "websectiga=6169c1e84f393779a5f7de7303038f3b47a78e47be716e7bec57ccce17d45f99; "
                  "sec_poison_id=ae001863-a9db-4463-ad78-ede3aac4e5b1; gid=yYD0jDJDWyU4yYD0jDJDJv1fqSlj7E3xu40fSvVTd"
                  "DEMEk2882kY7M888y4yJ4Y8D8SK0iiK; web_session=030037a2797dde5008c3e66f32224a8af75429; ",
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


class XHSDownloader(App):
    VERSION = 1.5
    Beta = True
    CSS_PATH = "static/XHS-Downloader.tcss"
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序"),
        ("d", "toggle_dark", "切换主题"),
    ]
    APP = XHS(**Settings().run())
    Batch = Batch()

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(Label("请输入小红书图文/视频作品链接："),
                                  Input(placeholder="URL"),
                                  HorizontalScroll(Button("下载无水印图片/视频", id="solo"),
                                                   Button("读取 xhs.txt 文件并批量下载作品", id="batch"),
                                                   Button("清空输入框", id="reset"), ))
        yield Log(auto_scroll=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"小红书作品采集工具 V{self.VERSION}{" Beta" if self.Beta else ""}"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "solo":
            self.solo()
        elif event.button.id == "batch":
            self.batch()
        elif event.button.id == "reset":
            self.query_one(Input).value = ""

    def solo(self):
        url = self.query_one(Input).value
        log = self.query_one(Log)
        log.write_line(f"当前作品链接: {url}")
        self.APP.extract(url, True, log)

    def batch(self):
        urls = self.Batch.read_txt()
        log = self.query_one(Log)
        if not urls:
            log.write_line("未检测到 xhs.txt 文件 或者 该文件为空！")
        for url in urls:
            log.write_line(f"当前作品链接: {url}")
            self.APP.extract(url, True, log)

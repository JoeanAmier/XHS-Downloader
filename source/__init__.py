from pathlib import Path
from re import compile

from pyperclip import paste
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

from .Downloader import Download
from .Explore import Explore
from .Html import Html
from .Image import Image
from .Manager import Manager
from .Settings import Settings
from .Video import Video

__all__ = ['XHS', 'XHSDownloader']


class XHS:
    ROOT = Path(__file__).resolve().parent.parent
    link = compile(r"https://www\.xiaohongshu\.com/explore/[a-z0-9]+")
    share = compile(r"https://www\.xiaohongshu\.com/discovery/item/[a-z0-9]+")
    short = compile(r"https://xhslink\.com/[A-Za-z0-9]+")

    def __init__(
            self,
            path="",
            folder="Download",
            proxies=None,
            timeout=10,
            chunk=1024 * 1024,
            **kwargs,
    ):
        self.manager = Manager(self.ROOT)
        self.html = Html(self.manager.headers, proxies, timeout)
        self.image = Image()
        self.video = Video()
        self.explore = Explore()
        self.download = Download(
            self.manager,
            self.ROOT,
            path,
            folder,
            proxies,
            chunk,
            timeout)

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

    def extract(self, url: str, download=False) -> list[dict]:
        urls = self.__deal_links(url)
        # return urls
        return [self.__deal_extract(i, download) for i in urls]

    def __deal_links(self, url: str) -> list:
        urls = []
        for i in url.split():
            if u := self.short.search(i):
                i = self.html.request_url(u.group(), headers=self.manager.headers, text=False)
            if u := self.share.search(i):
                urls.append(u.group())
            elif u := self.link.search(i):
                urls.append(u.group())
        return urls

    def __deal_extract(self, url: str, download: bool):
        html = self.html.request_url(url)
        if not html:
            return {}
        data = self.explore.run(html)
        if not data:
            return {}
        if data["作品类型"] == "视频":
            self.__get_video(data, html, download)
        else:
            self.__get_image(data, html, download)
        return data

    @staticmethod
    def __naming_rules(data: dict) -> str:
        """下载文件默认使用作品 ID 作为文件名，可修改此方法自定义文件名格式"""
        return data["作品ID"]


class XHSDownloader(App):
    VERSION = 1.6
    Beta = True
    ROOT = Path(__file__).resolve().parent.parent
    CSS_PATH = ROOT.joinpath(
        "static/XHS-Downloader.tcss")
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序"),
        ("d", "toggle_dark", "切换主题"),
    ]

    # APP = XHS(**Settings().run())

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(Label("请输入小红书图文/视频作品链接（多个链接使用空格分隔）："),
                                  Input(placeholder="URL"),
                                  HorizontalScroll(Button("下载无水印图片/视频", id="deal"),
                                                   Button("读取剪贴板", id="paste"),
                                                   Button("清空输入框", id="reset"), ))
        yield Log(auto_scroll=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"小红书作品采集工具 V{self.VERSION}{" Beta" if self.Beta else ""}"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "deal":
            self.deal()
        elif event.button.id == "reset":
            self.query_one(Input).value = ""
        elif event.button.id == "paste":
            self.query_one(Input).value = paste()

    def deal(self):
        url = self.query_one(Input).value
        log = self.query_one(Log)
        if not url:
            log.write_line("未输入任何作品链接！")
        else:
            self.APP.extract(url, True, log)
            self.query_one(Input).value = ""


class FakeGUI:
    pass

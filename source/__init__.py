from pathlib import Path
from re import compile

from pyperclip import paste
from rich.text import Text
from textual.app import App
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center
from textual.containers import HorizontalScroll
from textual.containers import ScrollableContainer
from textual.widgets import Button
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import ProgressBar
from textual.widgets import RichLog

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
    LINK = compile(r"https://www\.xiaohongshu\.com/explore/[a-z0-9]+")
    SHARE = compile(r"https://www\.xiaohongshu\.com/discovery/item/[a-z0-9]+")
    SHORT = compile(r"https://xhslink\.com/[A-Za-z0-9]+")
    __INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if not cls.__INSTANCE:
            cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE

    def __init__(
            self,
            path="",
            folder="Download",
            user_agent: str = None,
            proxy: str = None,
            timeout=10,
            chunk=1024 * 1024,
            **kwargs,
    ):
        self.manager = Manager(self.ROOT, user_agent)
        self.html = Html(self.manager.headers, proxy, timeout)
        self.image = Image()
        self.video = Video()
        self.explore = Explore()
        self.download = Download(
            self.manager,
            self.ROOT,
            path,
            folder,
            proxy,
            chunk,
            timeout)

    async def __get_image(self, container: dict, html: str, download, log, bar):
        urls = self.image.get_image_link(html)
        # self.rich_log(log, urls)  # 调试代码
        if download:
            await self.download.run(urls, self.__naming_rules(container), 1, log, bar)
        container["下载地址"] = urls

    async def __get_video(self, container: dict, html: str, download, log, bar):
        url = self.video.get_video_link(html)
        # self.rich_log(log, url)  # 调试代码
        if download:
            await self.download.run(url, self.__naming_rules(container), 0, log, bar)
        container["下载地址"] = url

    async def extract(self, url: str, download=False, log=None, bar=None) -> list[dict]:
        # return  # 调试代码
        urls = await self.__deal_links(url)
        # self.rich_log(log, urls)  # 调试代码
        # return urls  # 调试代码
        return [await self.__deal_extract(i, download, log, bar) for i in urls]

    async def __deal_links(self, url: str) -> list:
        urls = []
        for i in url.split():
            if u := self.SHORT.search(i):
                i = await self.html.request_url(
                    u.group(), False)
            if u := self.SHARE.search(i):
                urls.append(u.group())
            elif u := self.LINK.search(i):
                urls.append(u.group())
        return urls

    async def __deal_extract(self, url: str, download: bool, log, bar):
        html = await self.html.request_url(url)
        # self.rich_log(log, html)  # 调试代码
        if not html:
            return {}
        data = self.explore.run(html)
        # self.rich_log(log, data)  # 调试代码
        if not data:
            return {}
        if data["作品类型"] == "视频":
            await self.__get_video(data, html, download, log, bar)
        else:
            await self.__get_image(data, html, download, log, bar)
        return data

    @staticmethod
    def __naming_rules(data: dict) -> str:
        """下载文件默认使用作品 ID 作为文件名，可修改此方法自定义文件名格式"""
        return data["作品ID"]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.manager.clean()
        await self.html.session.close()
        await self.download.session.close()

    @staticmethod
    def rich_log(log, text, style="b bright_green"):
        if log:
            log.write(Text(text, style=style))
        else:
            print(text)


class XHSDownloader(App):
    VERSION = 1.6
    BETA = True
    ROOT = Path(__file__).resolve().parent.parent
    # APP = XHS(**Settings(ROOT).run())
    CSS_PATH = ROOT.joinpath(
        "static/XHS-Downloader.tcss")
    BINDINGS = [
        Binding(key="q", action="quit", description="结束运行"),
        ("d", "toggle_dark", "切换主题"),
    ]

    def __init__(self):
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.APP.manager.clean()

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(Label("请输入小红书图文/视频作品链接："),
                                  Input(placeholder="多个链接之间使用空格分隔"),
                                  HorizontalScroll(Button("下载无水印图片/视频", id="deal"),
                                                   Button("读取剪贴板", id="paste"),
                                                   Button("清空输入框", id="reset"), ),
                                  )
        with Center():
            yield ProgressBar(total=None)
        yield RichLog(markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"XHS-Downloader V{
        self.VERSION}{
        " Beta" if self.BETA else ""}"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "deal":
            self.deal()
        elif event.button.id == "reset":
            self.query_one(Input).value = ""
        elif event.button.id == "paste":
            self.query_one(Input).value = paste()

    def deal(self):
        url = self.query_one(Input)
        log = self.query_one(RichLog)
        bar = self.query_one(ProgressBar)
        if not url.value:
            log.write(Text("未输入任何小红书作品链接！", style="yellow"))
            return
        _ = self.APP.extract(url.value, True, log=log, bar=bar)
        if not _:
            log.write(Text("获取小红书作品数据失败！", style="red"))
        url.value = ""

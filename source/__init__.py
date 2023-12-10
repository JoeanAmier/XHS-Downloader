from pathlib import Path
from re import compile

from pyperclip import paste
from rich.text import Text
from textual.app import App
from textual.app import ComposeResult
from textual.binding import Binding
# from textual.containers import Center
from textual.containers import HorizontalScroll
from textual.containers import ScrollableContainer
from textual.widgets import Button
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Input
from textual.widgets import Label
# from textual.widgets import ProgressBar
from textual.widgets import RichLog

from .Downloader import Download
from .Explore import Explore
from .Html import Html
from .Image import Image
from .Manager import Manager
from .Settings import Settings
from .Video import Video

__all__ = ['XHS', 'XHSDownloader']

RELEASES = "https://github.com/JoeanAmier/XHS-Downloader/releases/latest"
VERSION = 1.7
BETA = True
ROOT = Path(__file__).resolve().parent.parent


class XHS:
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
            folder_name="Download",
            user_agent: str = None,
            cookie: str = None,
            proxy: str = "",
            timeout=10,
            chunk=1024 * 1024,
            max_retry=5,
            **kwargs,
    ):
        self.manager = Manager(ROOT, user_agent, cookie, max_retry)
        self.html = Html(
            self.manager.headers,
            proxy,
            timeout,
            self.manager.retry)
        self.image = Image()
        self.video = Video()
        self.explore = Explore()
        self.download = Download(
            self.manager,
            ROOT,
            path,
            folder_name,
            proxy,
            chunk,
            timeout,
            self.manager.retry, )
        self.rich_log = self.download.rich_log

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
        if not urls:
            self.rich_log(log, "提取小红书作品链接失败", "bright_red")
        else:
            self.rich_log(log, f"共 {len(urls)} 个小红书作品待处理")
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
        self.rich_log(log, f"开始处理：{url}")
        html = await self.html.request_url(url)
        # self.rich_log(log, html)  # 调试代码
        if not html:
            self.rich_log(log, f"{url} 获取数据失败", "bright_red")
            return {}
        data = self.explore.run(html)
        # self.rich_log(log, data)  # 调试代码
        if not data:
            self.rich_log(log, f"{url} 提取数据失败", "bright_red")
            return {}
        if data["作品类型"] == "视频":
            await self.__get_video(data, html, download, log, bar)
        else:
            await self.__get_image(data, html, download, log, bar)
        self.rich_log(log, f"完成处理：{url}")
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


class XHSDownloader(App):
    CSS_PATH = ROOT.joinpath(
        "static/XHS-Downloader.tcss")
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序"),
        ("d", "toggle_dark", "切换主题"),
        Binding(key="u", action="check_update", description="检查更新"),
    ]

    def __init__(self):
        super().__init__()
        self.APP = XHS(**Settings(ROOT).run())
        self.url = None
        self.log_ = None
        self.bar = None

    async def __aenter__(self):
        await self.APP.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.APP.__aexit__(exc_type, exc_value, traceback)

    def compose(self) -> ComposeResult:
        # yield LoadingIndicator()
        yield Header()
        yield ScrollableContainer(Label(Text("请输入小红书图文/视频作品链接：", style="b bright_blue")),
                                  Input(placeholder="多个链接之间使用空格分隔"),
                                  HorizontalScroll(Button("下载无水印图片/视频", id="deal"),
                                                   Button("读取剪贴板", id="paste"),
                                                   Button("清空输入框", id="reset"), ),
                                  # Label(Text("程序状态", style="b bright_blue")),
                                  )
        # with Center():
        #     yield ProgressBar(total=None)
        yield RichLog(markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"XHS-Downloader V{VERSION}{" Beta" if BETA else ""}"

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "deal":
            await self.deal()
        elif event.button.id == "reset":
            self.query_one(Input).value = ""
        elif event.button.id == "paste":
            self.query_one(Input).value = paste()

    async def deal(self):
        self.__init_objects()
        if not self.url.value:
            self.log_.write(Text("未输入任何小红书作品链接", style="b bright_yellow"))
            return
        if any(await self.APP.extract(self.url.value, True, log=self.log_, bar=self.bar)):
            self.url.value = ""
        else:
            self.log_.write(Text("下载小红书作品文件失败", style="b bright_red"))

    def __init_objects(self):
        if any((self.url, self.log_, self.bar)):
            return
        self.url = self.query_one(Input)
        self.log_ = self.query_one(RichLog)
        # self.bar = self.query_one(ProgressBar)

    async def action_check_update(self):
        self.__init_objects()
        try:
            url = await self.APP.html.request_url(RELEASES, False)
            tag = float(url.split("/")[-1])
            if tag > VERSION:
                self.log_.write(
                    Text(f"检测到新版本: {tag}", style="b bright_yellow"))
                self.log_.write(RELEASES)
            elif tag == VERSION and BETA:
                self.log_.write(
                    Text("当前版本为开发版, 可更新至正式版", style="b bright_yellow"))
                self.log_.write(RELEASES)
            elif BETA:
                self.log_.write(Text("当前已是最新开发版", style="b bright_yellow"))
            else:
                self.log_.write(Text("当前已是最新正式版", style="b bright_green"))
        except ValueError:
            self.log_.write(Text("检测新版本失败", style="b bright_red"))

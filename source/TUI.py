from webbrowser import open

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

from .App import XHS
from .Settings import Settings
from .Static import (
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_BETA,
    ROOT,
    PROMPT,
    MASTER,
    ERROR,
    WARNING,
    INFO,
    LICENCE,
    REPOSITORY,
    RELEASES,
    GENERAL,
    DISCLAIMER_TEXT,
    USERSCRIPT,
)

__all__ = ["XHSDownloader"]


def show_state(function):
    async def inner(self, *args, **kwargs):
        self.close_disclaimer()
        self.bar.update(total=100, progress=100)
        result = await function(self, *args, **kwargs)
        self.bar.update(total=None)
        self.tip.write(Text(">" * 50, style=GENERAL))
        return result

    return inner


class XHSDownloader(App):
    CSS_PATH = ROOT.joinpath(
        "static/XHS-Downloader.tcss")
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序"),
        # ("d", "toggle_dark", "切换主题"),
        Binding(key="u", action="check_update", description="检查更新"),
        Binding(key="m", action="user_script", description="获取脚本"),
    ]

    def __init__(self):
        super().__init__()
        self.APP = XHS(**Settings(ROOT).run())
        self.url = None
        self.tip = None
        self.bar = None
        self.disclaimer = True

    async def __aenter__(self):
        await self.APP.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.APP.__aexit__(exc_type, exc_value, traceback)

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(Label(Text(f"开源协议：{LICENCE}", style=MASTER)),
                                  Label(
                                      Text(
                                          f"项目地址：{REPOSITORY}",
                                          style=MASTER)),
                                  Label(Text("请输入小红书图文/视频作品链接：",
                                             style=PROMPT), id="prompt"),
                                  Input(placeholder="多个链接之间使用空格分隔"),
                                  HorizontalScroll(Button("下载无水印图片/视频", id="deal"),
                                                   Button("读取剪贴板", id="paste"),
                                                   Button("清空输入框", id="reset"), ),
                                  # Label(Text("准备就绪", style=INFO), id="state"),
                                  )
        with Center():
            yield ProgressBar(total=None, show_percentage=False, show_eta=False)
        yield RichLog(markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"XHS-Downloader V{VERSION_MAJOR}.{
        VERSION_MINOR}{" Beta" if VERSION_BETA else ""}"

    def on_ready(self) -> None:
        self.url = self.query_one(Input)
        self.tip = self.query_one(RichLog)
        self.bar = self.query_one(ProgressBar)
        self.tip.write(Text("\n".join(DISCLAIMER_TEXT), style=MASTER))

    def close_disclaimer(self):
        if self.disclaimer:
            self.tip.clear()
            self.disclaimer = False

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "deal":
            await self.deal()
        elif event.button.id == "reset":
            self.query_one(Input).value = ""
        elif event.button.id == "paste":
            self.query_one(Input).value = paste()

    @show_state
    async def deal(self):
        if not self.url.value:
            self.tip.write(Text("未输入任何小红书作品链接！", style=WARNING))
            return
        if any(await self.APP.extract(self.url.value, True, log=self.tip)):
            self.url.value = ""
        else:
            self.tip.write(Text("下载小红书作品文件失败！", style=ERROR))

    @show_state
    async def action_check_update(self):
        self.tip.write(Text("正在检查新版本，请稍等...", style=WARNING))
        try:
            url = await self.APP.html.request_url(RELEASES, False, self.tip)
            latest_major, latest_minor = map(
                int, url.split("/")[-1].split(".", 1))
            if latest_major > VERSION_MAJOR or latest_minor > VERSION_MINOR:
                self.tip.write(
                    Text(
                        f"检测到新版本：{latest_major}.{latest_minor}",
                        style=WARNING))
                self.tip.write(RELEASES)
            elif latest_minor == VERSION_MINOR and VERSION_BETA:
                self.tip.write(
                    Text("当前版本为开发版, 可更新至正式版！", style=WARNING))
                self.tip.write(RELEASES)
            elif VERSION_BETA:
                self.tip.write(Text("当前已是最新开发版！", style=WARNING))
            else:
                self.tip.write(Text("当前已是最新正式版！", style=INFO))
        except ValueError:
            self.tip.write(Text("检测新版本失败！", style=ERROR))

    @staticmethod
    def action_user_script():
        open(USERSCRIPT)

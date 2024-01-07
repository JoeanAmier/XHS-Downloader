from webbrowser import open

# from asyncio import sleep
from pyperclip import paste
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center
from textual.containers import HorizontalScroll
from textual.containers import ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import ProgressBar
from textual.widgets import RichLog

from source.application import XHS
from source.module import ROOT
from source.module import (
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_BETA,
    PROMPT,
    MASTER,
    ERROR,
    WARNING,
    INFO,
    LICENCE,
    REPOSITORY,
    RELEASES,
    GENERAL,
    USERSCRIPT,
)
from source.translator import (English, Chinese)

__all__ = ["Index"]


def show_state(function):
    async def inner(self, *args, **kwargs):
        self.close_disclaimer()
        self.bar.update(total=100, progress=100)
        result = await function(self, *args, **kwargs)
        self.bar.update(total=None)
        self.tip.write(Text(">" * 50, style=GENERAL))
        return result

    return inner


class Index(Screen):
    CSS_PATH = ROOT.joinpath(
        "static/css/index.tcss")
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序"),
        # ("d", "toggle_dark", "切换主题"),
        Binding(key="u", action="check_update", description="检查更新"),
        Binding(key="m", action="user_script", description="获取脚本"),
        Binding(key="s", action="settings", description="程序设置"),
    ]

    def __init__(self, app: XHS, language: Chinese | English):
        super().__init__()
        self.app_ = app
        self.prompt = language
        self.url = None
        self.tip = None
        self.bar = None
        self.disclaimer = True

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(Label(Text(f"{self.prompt.open_source_protocol}{LICENCE}", style=MASTER)),
                                  Label(
                                      Text(
                                          f"{self.prompt.project_address}{REPOSITORY}",
                                          style=MASTER)),
                                  Label(Text(self.prompt.input_box_title,
                                             style=PROMPT), id="prompt"),
                                  Input(placeholder=self.prompt.input_prompt),
                                  HorizontalScroll(Button(self.prompt.download_button, id="deal"),
                                                   Button(self.prompt.paste_button, id="paste"),
                                                   Button(self.prompt.reset_button, id="reset"), ),
                                  )
        with Center():
            yield ProgressBar(total=None, show_percentage=False, show_eta=False)
        yield RichLog(markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"XHS-Downloader V{VERSION_MAJOR}.{
        VERSION_MINOR}{" Beta" if VERSION_BETA else ""}"
        self.url = self.query_one(Input)
        self.tip = self.query_one(RichLog)
        self.bar = self.query_one(ProgressBar)
        self.tip.write(Text("\n".join(self.prompt.disclaimer), style=MASTER))

    def close_disclaimer(self):
        if self.disclaimer:
            self.tip.clear()
            self.disclaimer = False

    @on(Button.Pressed, "#deal")
    async def deal_button(self):
        await self.deal()

    @on(Button.Pressed, "#reset")
    def reset_button(self):
        self.query_one(Input).value = ""

    @on(Button.Pressed, "#paste")
    def paste_button(self):
        self.query_one(Input).value = paste()

    @show_state
    async def deal(self):
        # TODO: 处理过程中，进度条异常卡顿，待排查！
        # await sleep(2)
        if not self.url.value:
            self.tip.write(Text(self.prompt.invalid_link, style=WARNING))
            return
        if any(await self.app_.extract(self.url.value, True, log=self.tip)):
            self.url.value = ""
        else:
            self.tip.write(Text(self.prompt.download_failure, style=ERROR))

    @show_state
    async def action_check_update(self):
        self.tip.write(
            Text(
                self.prompt.check_update_notification,
                style=WARNING))
        try:
            url = await self.app_.html.request_url(RELEASES, False, self.tip)
            latest_major, latest_minor = map(
                int, url.split("/")[-1].split(".", 1))
            if latest_major > VERSION_MAJOR or latest_minor > VERSION_MINOR:
                self.tip.write(
                    Text(
                        self.prompt.official_version_update(
                            latest_major,
                            latest_minor),
                        style=WARNING))
                self.tip.write(RELEASES)
            elif latest_minor == VERSION_MINOR and VERSION_BETA:
                self.tip.write(
                    Text(
                        self.prompt.development_version_update,
                        style=WARNING))
                self.tip.write(RELEASES)
            elif VERSION_BETA:
                self.tip.write(
                    Text(
                        self.prompt.latest_development_version,
                        style=WARNING))
            else:
                self.tip.write(
                    Text(
                        self.prompt.latest_official_version,
                        style=INFO))
        except ValueError:
            self.tip.write(Text(self.prompt.check_update_failure, style=ERROR))

    @staticmethod
    def action_user_script():
        open(USERSCRIPT)

from asyncio import create_task
from webbrowser import open

from pyperclip import paste
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import HorizontalScroll
from textual.containers import ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import RichLog

from source.application import XHS
from source.module import (
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_BETA,
    PROMPT,
    MASTER,
    ERROR,
    WARNING,
    LICENCE,
    REPOSITORY,
    GENERAL,
    USERSCRIPT,
)
from source.translator import (
    English,
    Chinese,
)

__all__ = ["Index"]


class Index(Screen):
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序/Quit"),
        Binding(key="u", action="check_update", description="检查更新/Update"),
        Binding(key="m", action="user_script", description="获取脚本/Script"),
        Binding(key="s", action="settings", description="程序设置/Settings"),
    ]

    def __init__(self, app: XHS, language: Chinese | English):
        super().__init__()
        self.xhs = app
        self.prompt = language
        self.url = None
        self.tip = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Label(
                Text(
                    f"{self.prompt.open_source_protocol}{LICENCE}",
                    style=MASTER)
            ),
            Label(
                Text(
                    f"{self.prompt.project_address}{REPOSITORY}",
                    style=MASTER)
            ),
            Label(
                Text(
                    self.prompt.input_box_title,
                    style=PROMPT), id="prompt",
            ),
            Input(placeholder=self.prompt.input_prompt),
            HorizontalScroll(
                Button(self.prompt.download_button, id="deal"),
                Button(self.prompt.paste_button, id="paste"),
                Button(self.prompt.reset_button, id="reset"),
            ),
        )
        yield RichLog(markup=True, wrap=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"XHS-Downloader V{VERSION_MAJOR}.{
        VERSION_MINOR}{" Beta" if VERSION_BETA else ""}"
        self.url = self.query_one(Input)
        self.tip = self.query_one(RichLog)
        self.tip.write(Text("\n".join(self.prompt.disclaimer), style=MASTER))

    @on(Button.Pressed, "#deal")
    async def deal_button(self):
        if self.url.value:
            await create_task(self.deal())
        else:
            self.tip.write(Text(self.prompt.invalid_link, style=WARNING))
        self.tip.write(Text(">" * 50, style=GENERAL))

    @on(Button.Pressed, "#reset")
    def reset_button(self):
        self.query_one(Input).value = ""

    @on(Button.Pressed, "#paste")
    def paste_button(self):
        self.query_one(Input).value = paste()

    async def deal(self):
        await self.app.push_screen("loading")
        if any(await self.xhs.extract(self.url.value, True, log=self.tip)):
            self.url.value = ""
        else:
            self.tip.write(Text(self.prompt.download_failure, style=ERROR))
        self.app.pop_screen()

    @staticmethod
    def action_user_script():
        open(USERSCRIPT)

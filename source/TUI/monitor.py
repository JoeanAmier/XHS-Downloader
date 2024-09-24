from typing import Callable

from rich.text import Text
from textual import on
from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Button
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Label
from textual.widgets import RichLog

from ..application import XHS
from ..module import (
    PROJECT,
    MASTER,
    INFO,
)

__all__ = ["Monitor"]


class Monitor(Screen):
    BINDINGS = [
        Binding(key="Q", action="quit", description="退出程序/Quit"),
        Binding(key="C", action="close", description="关闭监听/Close"),
    ]

    def __init__(self, app: XHS, message: Callable[[str], str]):
        super().__init__()
        self.xhs = app
        self.message = message

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(Text(self.message("已启动监听剪贴板模式"), style=INFO), classes="prompt")
        yield RichLog(markup=True, wrap=True)
        yield Button(self.message("退出监听剪贴板模式"), id="close")
        yield Footer()

    @on(Button.Pressed, "#close")
    def close_button(self):
        self.action_close()

    @work()
    async def run_monitor(self):
        await self.xhs.monitor(download=True, log=self.query_one(RichLog), data=False, )
        self.action_close()

    def on_mount(self) -> None:
        self.title = PROJECT
        self.query_one(RichLog).write(
            Text(self.message(
                "程序会自动读取并提取剪贴板中的小红书作品链接，并自动下载链接对应的作品文件，如需关闭，请点击关闭按钮，或者向剪贴板写入 “close” 文本！"),
                style=MASTER))
        self.run_monitor()

    def action_close(self):
        self.xhs.stop_monitor()
        self.app.pop_screen()

    async def action_quit(self) -> None:
        self.action_close()
        await self.app.action_quit()

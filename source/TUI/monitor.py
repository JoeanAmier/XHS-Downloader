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

from source.application import XHS
from source.module import (
    PROJECT,
    MASTER,
    INFO,
)
from source.translator import (
    English,
    Chinese,
)

__all__ = ["Monitor"]


class Monitor(Screen):
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序/Quit"),
        Binding(key="c", action="close", description="关闭监听/Close"),
    ]

    def __init__(self, app: XHS, language: Chinese | English):
        super().__init__()
        self.xhs = app
        self.prompt = language

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(Text(self.prompt.monitor_mode, style=INFO), id="monitor")
        yield RichLog(markup=True, wrap=True)
        yield Button(self.prompt.close_monitor, id="close")
        yield Footer()

    @on(Button.Pressed, "#close")
    def close_button(self):
        self.action_close()

    @work()
    async def run_monitor(self):
        await self.xhs.monitor(download=True, log=self.query_one(RichLog))
        self.action_close()

    def on_mount(self) -> None:
        self.title = PROJECT
        self.query_one(RichLog).write(
            Text(self.prompt.monitor_text, style=MASTER))
        self.run_monitor()

    def action_close(self):
        self.xhs.stop_monitor()
        self.app.pop_screen()

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Label

from source.module import (
    PROJECT,
)
from source.translator import (
    Chinese,
    English,
)

__all__ = ["About"]


class About(Screen):
    BINDINGS = [
        Binding(
            key="q",
            action="quit",
            description="退出程序/Quit"),
        Binding(
            key="u",
            action="check_update_about",
            description="检查更新/Update"),
        Binding(
            key="b",
            action="index",
            description="返回首页/Back"),
    ]

    def __init__(self, language: Chinese | English):
        super().__init__()
        self.prompt = language

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label()
        yield Footer()

    def on_mount(self) -> None:
        self.title = PROJECT

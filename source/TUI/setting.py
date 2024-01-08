from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Label

from source.module import ROOT

__all__ = ["Setting"]


class Setting(Screen):
    CSS_PATH = ROOT.joinpath(
        "static/css/setting.tcss")
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序"),
        Binding(key="b", action="back", description="返回首页"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("我是设置页，敬请期待！")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "程序设置"

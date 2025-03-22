from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, RichLog

from ..application import XHS
from ..module import (
    INFO,
    MASTER,
    PROJECT,
)
from ..translation import _

__all__ = ["Monitor"]


class Monitor(Screen):
    BINDINGS = [
        Binding(key="Q", action="quit", description=_("退出程序")),
        Binding(key="C", action="close", description=_("关闭监听")),
    ]

    def __init__(
        self,
        app: XHS,
    ):
        super().__init__()
        self.xhs = app

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(Text(_("已启动监听剪贴板模式"), style=INFO), classes="prompt")
        yield RichLog(markup=True, wrap=True)
        yield Button(_("退出监听剪贴板模式"), id="close")
        yield Footer()

    @on(Button.Pressed, "#close")
    async def close_button(self):
        await self.action_close()

    @work(exclusive=True)
    async def run_monitor(self):
        await self.xhs.monitor(
            download=True,
            log=self.query_one(RichLog),
            data=False,
        )
        await self.action_close()

    def on_mount(self) -> None:
        self.title = PROJECT
        self.query_one(RichLog).write(
            Text(
                _(
                    "程序会自动读取并提取剪贴板中的小红书作品链接，并自动下载链接对应的作品文件，如需关闭，请点击关闭按钮，或者向剪贴板写入 “close” 文本！"
                ),
                style=MASTER,
            ),
            scroll_end=True,
        )
        self.run_monitor()

    async def action_close(self):
        self.xhs.stop_monitor()
        await self.app.action_back()

    async def action_quit(self) -> None:
        await self.action_close()
        await self.app.action_quit()

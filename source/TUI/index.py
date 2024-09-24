from typing import Callable

from pyperclip import paste
from rich.text import Text
from textual import on
from textual import work
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

from .monitor import Monitor
from ..application import XHS
from ..module import (
    PROJECT,
    PROMPT,
    MASTER,
    ERROR,
    WARNING,
    LICENCE,
    REPOSITORY,
    GENERAL,
)

__all__ = ["Index"]


class Index(Screen):
    BINDINGS = [
        Binding(key="Q", action="quit", description="退出程序/Quit"),
        Binding(key="U", action="update", description="检查更新/Update"),
        Binding(key="S", action="settings", description="程序设置/Settings"),
        Binding(key="R", action="record", description="下载记录/Record"),
        Binding(key="M", action="monitor", description="开启监听/Monitor"),
        Binding(key="A", action="about", description="关于项目/About"),
    ]

    def __init__(self, app: XHS, message: Callable[[str], str]):
        super().__init__()
        self.xhs = app
        self.message = message
        self.url = None
        self.tip = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Label(
                Text(
                    f"{self.message("开源协议")}: {LICENCE}",
                    style=MASTER)
            ),
            Label(
                Text(
                    f"{self.message("项目地址")}{REPOSITORY}",
                    style=MASTER)
            ),
            Label(
                Text(
                    self.message("请输入小红书图文/视频作品链接"),
                    style=PROMPT), classes="prompt",
            ),
            Input(placeholder=self.message("多个链接之间使用空格分隔")),
            HorizontalScroll(
                Button(self.message("下载无水印作品文件"), id="deal"),
                Button(self.message("读取剪贴板"), id="paste"),
                Button(self.message("清空输入框"), id="reset"),
            ),
        )
        yield RichLog(markup=True, )
        yield Footer()

    def on_mount(self) -> None:
        self.title = PROJECT
        self.url = self.query_one(Input)
        self.tip = self.query_one(RichLog)
        self.tip.write(
            Text(
                self.message("免责声明\n") +
                f"\n{
                ">" *
                50}",
                style=MASTER), scroll_end=False,
        )
        self.xhs.manager.print_proxy_tip(log=self.tip, )

    @on(Button.Pressed, "#deal")
    async def deal_button(self):
        if self.url.value:
            self.deal()
        else:
            self.tip.write(Text(self.message("未输入任何小红书作品链接"), style=WARNING))
            self.tip.write(Text(">" * 50, style=GENERAL))

    @on(Button.Pressed, "#reset")
    def reset_button(self):
        self.query_one(Input).value = ""

    @on(Button.Pressed, "#paste")
    def paste_button(self):
        self.query_one(Input).value = paste()

    @work()
    async def deal(self):
        await self.app.push_screen("loading")
        if any(await self.xhs.extract(self.url.value, True, log=self.tip, data=False, )):
            self.url.value = ""
        else:
            self.tip.write(Text(self.message("下载小红书作品文件失败"), style=ERROR))
        self.tip.write(Text(">" * 50, style=GENERAL))
        self.app.pop_screen()

    async def action_quit(self) -> None:
        await self.app.action_quit()

    async def action_update(self) -> None:
        await self.app.run_action("check_update")

    async def action_settings(self):
        await self.app.run_action("settings")

    async def action_monitor(self):
        await self.app.push_screen(Monitor(self.xhs, self.message))

    async def action_about(self):
        await self.app.push_screen("about")

    async def action_record(self):
        await self.app.push_screen("record")

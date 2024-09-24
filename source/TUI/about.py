from typing import Callable

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Label

from ..module import (
    PROJECT,
    PROMPT,
    MASTER,
    INFO,
)

__all__ = ["About"]


class About(Screen):
    BINDINGS = [
        Binding(
            key="Q",
            action="quit",
            description="退出程序/Quit"),
        Binding(
            key="U",
            action="check_update",
            description="检查更新/Update"),
        Binding(
            key="B",
            action="index",
            description="返回首页/Back"),
    ]

    def __init__(self, message: Callable[[str], str]):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(Text(self.message("如果 XHS-Downloader 对您有帮助，请考虑为它点个 Star，感谢您的支持！"), style=INFO),
                    classes="prompt", )
        yield Label(Text("Discord 社区", style=PROMPT), classes="prompt", )
        yield Label(f"{self.message("邀请链接：")}https://discord.com/invite/ZYtmgKud9Y")
        yield Label(Text(self.message("作者的其他开源项目"), style=PROMPT), classes="prompt", )
        yield Label(Text("TikTokDownloader (抖音 / TikTok)", style=MASTER), classes="prompt", )
        yield Label("https://github.com/JoeanAmier/TikTokDownloader")
        yield Label(Text("KS-Downloader (快手)", style=MASTER), classes="prompt", )
        yield Label("https://github.com/JoeanAmier/KS-Downloader")
        yield Footer()

    def on_mount(self) -> None:
        self.title = PROJECT

    async def action_quit(self) -> None:
        await self.app.action_quit()

    async def action_index(self):
        await self.app.push_screen("index")

    async def action_check_update(self):
        await self.app.run_action("update_and_return")

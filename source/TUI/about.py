from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Label
from textual.widgets import Link

from ..module import (
    PROJECT,
    PROMPT,
    MASTER,
    INFO,
)
from ..translation import _

__all__ = ["About"]


class About(Screen):
    BINDINGS = [
        Binding(
            key="Q",
            action="quit",
            description=_("退出程序")),
        Binding(
            key="U",
            action="check_update",
            description=_("检查更新")),
        Binding(
            key="B",
            action="index",
            description=_("返回首页")),
    ]

    def __init__(self, ):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(
            Text(
                _("如果 XHS-Downloader 对您有帮助，请考虑为它点个 Star，感谢您的支持！"),
                style=INFO,
            ),
            classes="prompt",
        )
        yield Label(Text(_("Discord 社区"), style=PROMPT), classes="prompt", )
        yield Link(
            _("邀请链接：") + "https://discord.com/invite/ZYtmgKud9Y",
            url="https://discord.com/invite/ZYtmgKud9Y",
            tooltip=_("点击访问"),
        )
        yield Label(Text(_("作者的其他开源项目"), style=PROMPT), classes="prompt", )
        yield Label(Text("TikTokDownloader (抖音 / TikTok)", style=MASTER), classes="prompt", )
        yield Link(
            "https://github.com/JoeanAmier/TikTokDownloader",
            url="https://github.com/JoeanAmier/TikTokDownloader",
            tooltip=_("点击访问"),
        )
        yield Label(Text("KS-Downloader (快手)", style=MASTER), classes="prompt", )
        yield Link(
            "https://github.com/JoeanAmier/KS-Downloader",
            url="https://github.com/JoeanAmier/KS-Downloader",
            tooltip=_("点击访问"),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = PROJECT

    async def action_quit(self) -> None:
        await self.app.action_quit()

    async def action_index(self):
        await self.app.push_screen("index")

    async def action_check_update(self):
        await self.app.run_action("update_and_return")

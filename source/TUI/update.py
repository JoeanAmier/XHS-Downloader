from typing import Callable

from aiohttp import ClientTimeout
from rich.text import Text
from textual import work
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Label
from textual.widgets import LoadingIndicator

from source.application import XHS
from source.module import (
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_BETA,
    ERROR,
    WARNING,
    INFO,
    RELEASES,
)

__all__ = ["Update"]


class Update(ModalScreen):
    def __init__(self, app: XHS, message: Callable[[str], str]):
        super().__init__()
        self.xhs = app
        self.message = message

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.message("正在检查新版本，请稍等...")),
            LoadingIndicator(),
            classes="loading",
        )

    @work()
    async def check_update(self) -> None:
        try:
            url = await self.xhs.html.request_url(RELEASES, False, None, timeout=ClientTimeout(connect=5))
            latest_major, latest_minor = map(
                int, url.split("/")[-1].split(".", 1))
            if latest_major > VERSION_MAJOR or latest_minor > VERSION_MINOR:
                tip = Text(f"{self.message("检测到新版本：{0}.{1}").format(
                    VERSION_MAJOR, VERSION_MINOR)}\n{RELEASES}", style=WARNING)
            elif latest_minor == VERSION_MINOR and VERSION_BETA:
                tip = Text(
                    f"{self.message("当前版本为开发版, 可更新至正式版")}\n{RELEASES}",
                    style=WARNING)
            elif VERSION_BETA:
                tip = Text(
                    self.message("当前已是最新开发版"),
                    style=WARNING)
            else:
                tip = Text(
                    self.message("当前已是最新正式版"),
                    style=INFO)
        except ValueError:
            tip = Text(self.message("检测新版本失败"), style=ERROR)
        self.dismiss(tip)

    def on_mount(self) -> None:
        self.check_update()

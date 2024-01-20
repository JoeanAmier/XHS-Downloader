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
from source.translator import (
    English,
    Chinese,
)

__all__ = ["Update"]


class Update(ModalScreen):
    def __init__(self, app: XHS, language: Chinese | English):
        super().__init__()
        self.xhs = app
        self.prompt = language

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.prompt.check_update_notification),
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
                tip = Text(
                    f"{self.prompt.official_version_update(
                        latest_major,
                        latest_minor)}\n{RELEASES}",
                    style=WARNING)
            elif latest_minor == VERSION_MINOR and VERSION_BETA:
                tip = Text(
                    f"{self.prompt.development_version_update}\n{RELEASES}",
                    style=WARNING)
            elif VERSION_BETA:
                tip = Text(
                    self.prompt.latest_development_version,
                    style=WARNING)
            else:
                tip = Text(
                    self.prompt.latest_official_version,
                    style=INFO)
        except ValueError:
            tip = Text(self.prompt.check_update_failure, style=ERROR)
        self.dismiss(tip)

    def on_mount(self) -> None:
        self.check_update()

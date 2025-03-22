from textual import work
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Label, LoadingIndicator

from ..application import XHS
from ..module import (
    RELEASES,
)
from ..translation import _

__all__ = ["Update"]


class Update(ModalScreen):
    def __init__(
        self,
        app: XHS,
    ):
        super().__init__()
        self.xhs = app

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(_("正在检查新版本，请稍等...")),
            LoadingIndicator(),
            classes="loading",
        )

    @work(exclusive=True)
    async def check_update(self) -> None:
        try:
            url = await self.xhs.html.request_url(
                RELEASES,
                False,
                None,
                timeout=5,
            )
            version = url.split("/")[-1]
            match self.compare_versions(
                f"{XHS.VERSION_MAJOR}.{XHS.VERSION_MINOR}", version, XHS.VERSION_BETA
            ):
                case 4:
                    args = (
                        _("检测到新版本：{0}.{1}").format(
                            XHS.VERSION_MAJOR,
                            XHS.VERSION_MINOR,
                        ),
                        "warning",
                    )
                case 3:
                    args = (
                        _("当前版本为开发版, 可更新至正式版"),
                        "warning",
                    )
                case 2:
                    args = (
                        _("当前已是最新开发版"),
                        "warning",
                    )
                case 1:
                    args = (
                        _("当前已是最新正式版"),
                        "information",
                    )
                case _:
                    raise ValueError
        except ValueError:
            args = (
                _("检测新版本失败"),
                "error",
            )
        self.dismiss(args)

    def on_mount(self) -> None:
        self.check_update()

    @staticmethod
    def compare_versions(
        current_version: str, target_version: str, is_development: bool
    ) -> int:
        current_major, current_minor = map(int, current_version.split("."))
        target_major, target_minor = map(int, target_version.split("."))

        if target_major > current_major:
            return 4
        if target_major == current_major:
            if target_minor > current_minor:
                return 4
            if target_minor == current_minor:
                return 3 if is_development else 1
        return 2

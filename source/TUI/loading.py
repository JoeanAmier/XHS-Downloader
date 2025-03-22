from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Label, LoadingIndicator

from ..translation import _

__all__ = ["Loading"]


class Loading(ModalScreen):
    def __init__(
        self,
    ):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(_("程序处理中...")),
            LoadingIndicator(),
            classes="loading",
        )

from typing import Callable

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Label
from textual.widgets import LoadingIndicator

__all__ = ["Loading"]


class Loading(ModalScreen):
    def __init__(self, message: Callable[[str], str]):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.message("程序处理中...")),
            LoadingIndicator(),
            classes="loading",
        )

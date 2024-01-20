from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Label
from textual.widgets import LoadingIndicator

from source.translator import (
    English,
    Chinese,
)

__all__ = ["Loading"]


class Loading(ModalScreen):
    def __init__(self, language: Chinese | English):
        super().__init__()
        self.prompt = language

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.prompt.processing),
            LoadingIndicator(),
            classes="loading",
        )

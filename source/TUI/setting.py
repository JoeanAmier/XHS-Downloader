from textual.app import ComposeResult
from textual.widgets import Label
from textual.widgets import Static

from source.module import ROOT

__all__ = ["Setting"]


class Setting(Static):
    CSS_PATH = ROOT.joinpath(
        "static/css/setting.tcss")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Label("我是设置页")

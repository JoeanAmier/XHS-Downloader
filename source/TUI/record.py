from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.containers import HorizontalScroll
from textual.screen import ModalScreen
from textual.widgets import Button
from textual.widgets import Input
from textual.widgets import Label

from source.application import XHS
from source.translator import (
    Chinese,
    English,
)

__all__ = ["Record"]


class Record(ModalScreen):
    def __init__(self, app: XHS, language: Chinese | English):
        super().__init__()
        self.xhs = app
        self.prompt = language

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.prompt.record_title, classes="prompt"),
            Input(placeholder=self.prompt.record_placeholder, id="id", ),
            HorizontalScroll(
                Button(self.prompt.record_enter_button, id="enter", ),
                Button(self.prompt.record_close_button, id="close"), ),
            id="record",
        )

    async def delete(self, text: str):
        await self.xhs.recorder.delete_many(text.split())

    @on(Button.Pressed, "#enter")
    async def save_settings(self):
        text = self.query_one(Input)
        await self.delete(text.value)
        text.value = ""

    @on(Button.Pressed, "#close")
    def reset(self):
        self.dismiss()

from typing import Callable

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.containers import HorizontalScroll
from textual.screen import ModalScreen
from textual.widgets import Button
from textual.widgets import Input
from textual.widgets import Label

from ..application import XHS

__all__ = ["Record"]


class Record(ModalScreen):
    def __init__(self, app: XHS, message: Callable[[str], str]):
        super().__init__()
        self.xhs = app
        self.message = message

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.message("请输入待删除的小红书作品链接或作品 ID"), classes="prompt"),
            Input(placeholder=self.message("支持输入作品 ID 或包含作品 ID 的作品链接，多个链接或 ID 之间使用空格分隔"),
                  id="id", ),
            HorizontalScroll(
                Button(self.message("删除指定作品 ID"), id="enter", ),
                Button(self.message("返回首页"), id="close"), ),
            id="record",
        )

    async def delete(self, text: str):
        await self.xhs.id_recorder.delete(text)

    @on(Button.Pressed, "#enter")
    async def save_settings(self):
        text = self.query_one(Input)
        await self.delete(text.value)
        text.value = ""

    @on(Button.Pressed, "#close")
    def reset(self):
        self.dismiss()

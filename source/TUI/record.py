from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, HorizontalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label

from ..application import XHS
from ..translation import _

__all__ = ["Record"]


class Record(ModalScreen):
    def __init__(
        self,
        app: XHS,
    ):
        super().__init__()
        self.xhs = app

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(_("请输入待删除的小红书作品链接或作品 ID"), classes="prompt"),
            Input(
                placeholder=_(
                    "支持输入作品 ID 或包含作品 ID 的作品链接，多个链接或 ID 之间使用空格分隔"
                ),
                id="id",
            ),
            HorizontalScroll(
                Button(
                    _("删除指定作品 ID"),
                    id="enter",
                ),
                Button(_("返回首页"), id="close"),
            ),
            id="record",
        )

    async def delete(self, text: str):
        text = await self.xhs.extract_links(
            text,
            None,
        )
        text = self.xhs.extract_id(text)
        await self.xhs.id_recorder.delete(text)
        self.app.notify(_("删除下载记录成功"))

    @on(Button.Pressed, "#enter")
    async def save_settings(self):
        text = self.query_one(Input)
        await self.delete(text.value)
        text.value = ""

    @on(Button.Pressed, "#close")
    def reset(self):
        self.dismiss()

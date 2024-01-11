from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.containers import ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button
from textual.widgets import Checkbox
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import Select

from source.module import ROOT

__all__ = ["Setting"]


class Setting(Screen):
    CSS_PATH = ROOT.joinpath("static/XHS-Downloader.tcss")
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序"),
        Binding(key="b", action="index", description="返回首页"),
    ]

    def __init__(self, data: dict):
        super().__init__()
        self.data = data

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Label("工作路径：", classes="params", ),
            Input(self.data["work_path"], placeholder="程序根路径", valid_empty=True, id="work_path", ),
            Label("文件夹名称：", classes="params", ),
            Input(self.data["folder_name"], placeholder="Download", id="folder_name", ),
            Label("User-Agent：", classes="params", ),
            Input(self.data["user_agent"], placeholder="默认 UA", valid_empty=True, id="user_agent", ),
            Label("Cookie：", classes="params", ),
            Input(self.data["cookie"], placeholder="内置 Cookie，建议自行设置", valid_empty=True, id="cookie", ),
            Label("网络代理：", classes="params", ),
            Input(self.data["proxy"], placeholder="无代理", valid_empty=True, id="proxy", ),
            Label("请求超时限制：", classes="params", ),
            Input(str(self.data["timeout"]), placeholder="10", type="integer", id="timeout", ),
            Label("数据块大小：", classes="params", ),
            Input(str(self.data["chunk"]), placeholder="1048576", type="integer", id="chunk", ),
            Label("最大重试次数：", classes="params", ),
            Input(str(self.data["max_retry"]), placeholder="5", type="integer", id="max_retry", ),
            Container(
                Label("", classes="params", ),
                Label("", classes="params", ),
                Label("图片下载格式", classes="params", ),
                Label("程序语言", classes="params", ),
                classes="horizontal-layout",
            ),
            Container(
                Checkbox("记录作品数据", id="record_data", value=self.data["record_data"], ),
                Checkbox("文件夹归档模式", id="folder_mode", value=self.data["folder_mode"], ),
                Select.from_values(
                    ("PNG", "WEBP"),
                    value=self.data["image_format"],
                    allow_blank=False,
                    id="image_format"),
                Select.from_values(("zh-CN", "en-US"),
                                   value=self.data["language"],
                                   allow_blank=False,
                                   id="language",
                                   disabled=True, ),
                classes="horizontal-layout"),
            Container(
                Button("保存设置", id="save", ),
                Button("放弃更改", id="abandon", ),
                classes="settings_button", ),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = "程序设置"

    @on(Button.Pressed, "#save")
    def save_settings(self):
        self.dismiss({
            "work_path": self.query_one("#work_path").value,
            "folder_name": self.query_one("#folder_name").value,
            "user_agent": self.query_one("#user_agent").value,
            "cookie": self.query_one("#cookie").value,
            "proxy": self.query_one("#proxy").value or None,
            "timeout": int(self.query_one("#timeout").value),
            "chunk": int(self.query_one("#chunk").value),
            "max_retry": int(self.query_one("#max_retry").value),
            "record_data": self.query_one("#record_data").value,
            "image_format": self.query_one("#image_format").value,
            "folder_mode": self.query_one("#folder_mode").value,
            "language": self.query_one("#language").value,
        })

    @on(Button.Pressed, "#abandon")
    def reset(self):
        self.dismiss(self.data)

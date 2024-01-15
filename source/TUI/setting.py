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
from source.translator import (
    LANGUAGE,
    Chinese,
    English,
)

__all__ = ["Setting"]


class Setting(Screen):
    CSS_PATH = ROOT.joinpath("static/XHS-Downloader.tcss")
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序/Quit"),
        Binding(key="b", action="index", description="返回首页/Back"),
    ]

    def __init__(self, data: dict, language: Chinese | English):
        super().__init__()
        self.data = data
        self.prompt = language

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Label(self.prompt.work_path, classes="params", ),
            Input(self.data["work_path"], placeholder=self.prompt.work_path_placeholder, valid_empty=True,
                  id="work_path", ),
            Label(self.prompt.folder_name, classes="params", ),
            Input(self.data["folder_name"], placeholder="Download", id="folder_name", ),
            Label(self.prompt.user_agent, classes="params", ),
            Input(self.data["user_agent"], placeholder=self.prompt.user_agent_placeholder, valid_empty=True,
                  id="user_agent", ),
            Label(self.prompt.cookie, classes="params", ),
            Input(self.data["cookie"], placeholder=self.prompt.cookie_placeholder, valid_empty=True, id="cookie", ),
            Label(self.prompt.proxy, classes="params", ),
            Input(self.data["proxy"], placeholder=self.prompt.proxy_placeholder, valid_empty=True, id="proxy", ),
            Label(self.prompt.timeout, classes="params", ),
            Input(str(self.data["timeout"]), placeholder="10", type="integer", id="timeout", ),
            Label(self.prompt.chunk, classes="params", ),
            Input(str(self.data["chunk"]), placeholder="1048576", type="integer", id="chunk", ),
            Label(self.prompt.max_retry, classes="params", ),
            Input(str(self.data["max_retry"]), placeholder="5", type="integer", id="max_retry", ),
            Container(
                Label("", classes="params", ),
                Label("", classes="params", ),
                Label(self.prompt.image_format, classes="params", ),
                Label(self.prompt.language, classes="params", ),
                classes="horizontal-layout",
            ),
            Container(
                Checkbox(self.prompt.record_data, id="record_data", value=self.data["record_data"], ),
                Checkbox(self.prompt.folder_mode, id="folder_mode", value=self.data["folder_mode"], ),
                Select.from_values(
                    ("PNG", "WEBP"),
                    value=self.data["image_format"],
                    allow_blank=False,
                    id="image_format"),
                Select.from_values(list(LANGUAGE.keys()),
                                   value=self.data["language"],
                                   allow_blank=False,
                                   id="language", ),
                classes="horizontal-layout"),
            Container(
                Button(self.prompt.save_button, id="save", ),
                Button(self.prompt.abandon_button, id="abandon", ),
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

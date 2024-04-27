from typing import Callable

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

__all__ = ["Setting"]


class Setting(Screen):
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序/Quit"),
        Binding(key="b", action="index", description="返回首页/Back"),
    ]

    def __init__(self, data: dict, message: Callable[[str], str]):
        super().__init__()
        self.data = data
        self.message = message

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Label(self.message("作品数据 / 文件保存根路径"), classes="params", ),
            Input(self.data["work_path"], placeholder=self.message("程序根路径"), valid_empty=True,
                  id="work_path", ),
            Label(self.message("作品文件储存文件夹名称"), classes="params", ),
            Input(self.data["folder_name"], placeholder="Download", id="folder_name", ),
            Label(self.message("作品文件名称格式"), classes="params", ),
            Input(self.data["name_format"], placeholder=self.message("发布时间 作者昵称 作品标题"), valid_empty=True,
                  id="name_format", ),
            Label(self.message("User-Agent"), classes="params", ),
            Input(self.data["user_agent"], placeholder=self.message("默认 User-Agent"), valid_empty=True,
                  id="user_agent", ),
            Label(self.message("小红书网页版 Cookie"), classes="params", ),
            Input(placeholder=self.__check_cookie(), valid_empty=True, id="cookie", ),
            Label(self.message("网络代理"), classes="params", ),
            Input(self.data["proxy"], placeholder=self.message("不使用代理"), valid_empty=True, id="proxy", ),
            Label(self.message("请求数据超时限制，单位：秒"), classes="params", ),
            Input(str(self.data["timeout"]), placeholder="10", type="integer", id="timeout", ),
            Label(self.message("下载文件时，每次从服务器获取的数据块大小，单位：字节"), classes="params", ),
            Input(str(self.data["chunk"]), placeholder="1048576", type="integer", id="chunk", ),
            Label(self.message("请求数据失败时，重试的最大次数"), classes="params", ),
            Input(str(self.data["max_retry"]), placeholder="5", type="integer", id="max_retry", ),
            Container(
                Checkbox(self.message("记录作品数据"), id="record_data", value=self.data["record_data"], ),
                Checkbox(self.message("作品文件夹归档模式"), id="folder_mode", value=self.data["folder_mode"], ),
                Checkbox(self.message("视频作品下载开关"), id="video_download", value=self.data["video_download"], ),
                Checkbox(self.message("图文作品下载开关"), id="image_download", value=self.data["image_download"], ),
                classes="horizontal-layout"),
            Container(
                Label(self.message("图片下载格式"), classes="params", ),
                Label(self.message("程序语言"), classes="params", ),
                classes="horizontal-layout",
            ),
            Container(
                Select.from_values(
                    ("PNG", "WEBP"),
                    value=self.data["image_format"],
                    allow_blank=False,
                    id="image_format"),
                Select.from_values(["zh_CN", "en_GB"],
                                   value=self.data["language"],
                                   allow_blank=False,
                                   id="language", ),
                classes="horizontal-layout"),
            Container(
                Button(self.message("保存配置"), id="save", ),
                Button(self.message("放弃更改"), id="abandon", ),
                classes="settings_button", ),
        )
        yield Footer()

    def __check_cookie(self) -> str:
        if self.data["cookie"]:
            return self.message("小红书网页版 Cookie，无需登录，参数已设置")
        return self.message("小红书网页版 Cookie，无需登录，参数未设置")

    def on_mount(self) -> None:
        self.title = self.message("程序设置")

    @on(Button.Pressed, "#save")
    def save_settings(self):
        self.dismiss({
            "work_path": self.query_one("#work_path").value,
            "folder_name": self.query_one("#folder_name").value,
            "name_format": self.query_one("#name_format").value,
            "user_agent": self.query_one("#user_agent").value,
            "cookie": self.query_one("#cookie").value or self.data["cookie"],
            "proxy": self.query_one("#proxy").value or None,
            "timeout": int(self.query_one("#timeout").value),
            "chunk": int(self.query_one("#chunk").value),
            "max_retry": int(self.query_one("#max_retry").value),
            "record_data": self.query_one("#record_data").value,
            "image_format": self.query_one("#image_format").value,
            "folder_mode": self.query_one("#folder_mode").value,
            "language": self.query_one("#language").value,
            "image_download": self.query_one("#image_download").value,
            "video_download": self.query_one("#video_download").value,
            "server": False,
        })

    @on(Button.Pressed, "#abandon")
    def reset(self):
        self.dismiss(self.data)

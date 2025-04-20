from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Footer, Header, Input, Label, Select

from ..translation import _

__all__ = ["Setting"]


class Setting(Screen):
    BINDINGS = [
        Binding(key="Q", action="quit", description=_("退出程序")),
        Binding(key="B", action="index", description=_("返回首页")),
    ]

    def __init__(
        self,
        data: dict,
    ):
        super().__init__()
        self.data = data

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Label(
                _("作品数据 / 文件保存根路径"),
                classes="params",
            ),
            Input(
                self.data["work_path"],
                placeholder=_("程序根路径"),
                valid_empty=True,
                id="work_path",
            ),
            Label(
                _("作品文件储存文件夹名称"),
                classes="params",
            ),
            Input(
                self.data["folder_name"],
                placeholder="Download",
                id="folder_name",
            ),
            Label(
                _("作品文件名称格式"),
                classes="params",
            ),
            Input(
                self.data["name_format"],
                placeholder="发布时间 作者昵称 作品标题",
                valid_empty=True,
                id="name_format",
            ),
            Label(
                "User-Agent",
                classes="params",
            ),
            Input(
                self.data["user_agent"],
                placeholder=_("内置 Chrome User Agent"),
                valid_empty=True,
                id="user_agent",
            ),
            Label(
                _("小红书网页版 Cookie"),
                classes="params",
            ),
            Input(
                placeholder=self.__check_cookie(),
                valid_empty=True,
                id="cookie",
            ),
            Label(
                _("网络代理"),
                classes="params",
            ),
            Input(
                self.data["proxy"],
                placeholder=_("不使用代理"),
                valid_empty=True,
                id="proxy",
            ),
            Label(
                _("请求数据超时限制，单位：秒"),
                classes="params",
            ),
            Input(
                str(self.data["timeout"]),
                placeholder="10",
                type="integer",
                id="timeout",
            ),
            Label(
                _("下载文件时，每次从服务器获取的数据块大小，单位：字节"),
                classes="params",
            ),
            Input(
                str(self.data["chunk"]),
                placeholder="1048576",
                type="integer",
                id="chunk",
            ),
            Label(
                _("请求数据失败时，重试的最大次数"),
                classes="params",
            ),
            Input(
                str(self.data["max_retry"]),
                placeholder="5",
                type="integer",
                id="max_retry",
            ),
            Label(),
            Container(
                Checkbox(
                    _("记录作品详细数据"),
                    id="record_data",
                    value=self.data["record_data"],
                ),
                Checkbox(
                    _("作品归档保存模式"),
                    id="folder_mode",
                    value=self.data["folder_mode"],
                ),
                Checkbox(
                    _("视频作品下载开关"),
                    id="video_download",
                    value=self.data["video_download"],
                ),
                Checkbox(
                    _("图文作品下载开关"),
                    id="image_download",
                    value=self.data["image_download"],
                ),
                classes="horizontal-layout",
            ),
            Label(),
            Container(
                Checkbox(
                    _("动图文件下载开关"),
                    id="live_download",
                    value=self.data["live_download"],
                ),
                Checkbox(
                    _("作品下载记录开关"),
                    id="download_record",
                    value=self.data["download_record"],
                ),
                Checkbox(
                    _("作者归档保存模式"),
                    id="author_archive",
                    value=self.data["author_archive"],
                ),
                Checkbox(
                    _("更新文件修改时间"),
                    id="write_mtime",
                    value=self.data["write_mtime"],
                ),
                classes="horizontal-layout",
            ),
            Container(
                Label(
                    _("图片下载格式"),
                    classes="params",
                ),
                Label(
                    _("程序语言"),
                    classes="params",
                ),
                classes="horizontal-layout",
            ),
            Label(),
            Container(
                Select.from_values(
                    ("AUTO", "PNG", "WEBP", "JPEG", "HEIC"),
                    value=self.data["image_format"].upper(),
                    allow_blank=False,
                    id="image_format",
                ),
                Select.from_values(
                    ["zh_CN", "en_US"],
                    value=self.data["language"],
                    allow_blank=False,
                    id="language",
                ),
                classes="horizontal-layout",
            ),
            Container(
                Button(
                    _("保存配置"),
                    id="save",
                ),
                Button(
                    _("放弃更改"),
                    id="abandon",
                ),
                classes="settings_button",
            ),
        )
        yield Footer()

    def __check_cookie(self) -> str:
        if self.data["cookie"]:
            return _("小红书网页版 Cookie，无需登录，参数已设置")
        return _("小红书网页版 Cookie，无需登录，参数未设置")

    def on_mount(self) -> None:
        self.title = _("程序设置")

    @on(Button.Pressed, "#save")
    def save_settings(self):
        self.dismiss(
            {
                "mapping_data": self.data.get("mapping_data", {}),
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
                "live_download": self.query_one("#live_download").value,
                "download_record": self.query_one("#download_record").value,
                "author_archive": self.query_one("#author_archive").value,
                "write_mtime": self.query_one("#write_mtime").value,
            }
        )

    @on(Button.Pressed, "#abandon")
    def reset(self):
        self.dismiss(self.data)

    async def action_quit(self) -> None:
        await self.app.action_quit()

    async def action_index(self):
        await self.app.action_back()

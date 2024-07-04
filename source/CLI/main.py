from asyncio import run
from contextlib import suppress
from pathlib import Path as Root
from textwrap import fill

from click import Context
from click import (
    command,
    option,
    Path,
    Choice,
    pass_context,
    echo,
)
from rich import print
from rich.panel import Panel
from rich.table import Table

from source.application import XHS
from source.expansion import BrowserCookie
from source.module import (
    ROOT,
    PROJECT,
)
from source.module import Settings
from source.module import Translate

__all__ = ["cli"]


def check_value(function):
    def inner(ctx: Context, param, value):
        if not value:
            return
        return function(ctx, param, value)

    return inner


class CLI:
    def __init__(self, ctx: Context, **kwargs):
        # print(kwargs)
        self.ctx = ctx
        self.url = kwargs.pop("url")
        self.index = self.__format_index(kwargs.pop("index"))
        self.path = kwargs.pop("settings")
        self.update = kwargs.pop("update_settings")
        # print(kwargs)
        self.settings = Settings(self.__check_settings_path())
        self.parameter = self.settings.run() | self.__clean_params(kwargs)
        self.APP = XHS(**self.parameter)

    async def __aenter__(self):
        await self.APP.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.APP.__aexit__(exc_type, exc_value, traceback)

    async def run(self):
        if self.url:
            await self.APP.extract_cli(self.url, index=self.index)
        self.__update_settings()

    def __update_settings(self):
        if self.update:
            self.settings.update(self.parameter)

    def __check_settings_path(self) -> Path:
        if not self.path:
            return ROOT
        return s.parent if (s := Root(self.path)).is_file() else ROOT

    @staticmethod
    def __merge_cookie(data: dict) -> None:
        if not data["cookie"] and (bc := data["browser_cookie"]):
            data["cookie"] = bc
        data.pop("browser_cookie")

    def __clean_params(self, data: dict) -> dict:
        self.__merge_cookie(data)
        return {k: v for k, v in data.items() if v}

    @staticmethod
    def __format_index(index: str) -> list:
        if index:
            result = []
            values = index.split()
            for i in values:
                with suppress(ValueError):
                    result.append(int(i))
            return result
        return []

    @staticmethod
    @check_value
    def version(ctx: Context, param, value) -> None:
        echo(PROJECT)
        ctx.exit()

    @staticmethod
    @check_value
    def read_cookie(ctx: Context, param, value) -> str:
        if len(value) == 1:
            value = int(value)
        return BrowserCookie.get(value, domain="xiaohongshu.com")

    @staticmethod
    @check_value
    def help_(ctx: Context, param, value) -> None:
        _ = Translate("").message()
        table = Table(highlight=True, box=None, show_header=True)

        # 添加表格的列名
        table.add_column("parameter", no_wrap=True, style="bold")
        table.add_column("abbreviation", no_wrap=True, style="bold")
        table.add_column("type", no_wrap=True, style="bold")
        table.add_column("description", no_wrap=True, )

        # TODO: 语言设置未生效
        options = (
            ("--url", "-u", "str", _("小红书作品链接")),
            ("--index", "-i", "str", _("下载指定序号的图片文件，仅对图文作品生效；多个序号输入示例：\"1 3 5 7\"")),
            ("--work_path", "-wp", "str", _("作品数据 / 文件保存根路径")),
            ("--folder_name", "-fn", "str", _("作品文件储存文件夹名称")),
            ("--name_format", "-nf", "str", _("作品文件名称格式")),
            ("--sec_ch_ua", "-su", "str", _("Sec-Ch-Ua")),
            ("--sec_ch_ua_platform", "-sp", "str", _("User-Agent")),
            ("--user_agent", "-ua", "str", _("Sec-Ch-Ua-Platform")),
            ("--cookie", "-ck", "str", _("小红书网页版 Cookie，无需登录")),
            ("--proxy", "-p", "str", _("网络代理")),
            ("--timeout", "-t", "int", _("请求数据超时限制，单位：秒")),
            ("--chunk", "-c", "int", _("下载文件时，每次从服务器获取的数据块大小，单位：字节")),
            ("--max_retry", "-mr", "int", _("请求数据失败时，重试的最大次数")),
            ("--record_data", "-rd", "bool", _("是否记录作品数据至文件")),
            ("--image_format", "-if", "choice", _("图文作品文件下载格式，支持：PNG、WEBP")),
            ("--live_download", "-ld", "bool", _("图文动图文件下载开关")),
            ("--folder_mode", "-fm", "bool", _("是否将每个作品的文件储存至单独的文件夹")),
            ("--language", "-l", "choice", _("设置程序语言，目前支持：zh_CN、en_GB")),
            ("--settings", "-s", "str", _("读取指定配置文件")),
            ("--browser_cookie", "-bc", "choice",
             fill(_("从指定的浏览器读取小红书网页版 Cookie，需要关闭对应的浏览器，支持：1 Chrome, 2 Chromium, 3 Opera, 4 Opera GX, "
                    "5 Brave, 6 Edge, 7 Vivaldi, 8 Firefox, 9 LibreWolf, 10 Safari，输入浏览器类型或序号"), width=45)),
            ("--update_settings", "-us", "flag", _("是否更新配置文件")),
            ("--help", "-h", "flag", _("查看详细参数说明")),
            ("--version", "-v", "flag", _("查看 XHS-Downloader 版本")),
        )

        for option in options:
            table.add_row(*option)

        print(
            Panel(
                table,
                border_style="bold",
                title="XHS-Downloader CLI Parameters",
                title_align="left"))
        ctx.exit()


@command(name="XHS-Downloader", help=PROJECT)
@option("--url", "-u", )
@option("--index", "-i", )
@option("--work_path",
        "-wp",
        type=Path(file_okay=False),
        )
@option("--folder_name", "-fn", )
@option("--name_format", "-nf", )
@option("--sec_ch_ua", "-su", )
@option("--sec_ch_ua_platform", "-sp", )
@option("--user_agent", "-ua", )
@option("--cookie", "-ck", )
@option("--proxy", "-p", )
@option("--timeout", "-t", type=int, )
@option("--chunk", "-c", type=int, )
@option("--max_retry", "-mr", type=int, )
@option("--record_data", "-rd", type=bool, )
@option("--image_format", "-if", type=Choice(["png", "PNG", "webp", "WEBP"]), )
@option("--live_download", "-ld", type=bool, )
@option("--folder_mode", "-fm", type=bool, )
@option("--language", "-l",
        type=Choice(["zh_CN", "en_GB"]), )
@option("--settings", "-s", type=Path(dir_okay=False), )
@option("--browser_cookie", "-bc", type=Choice(list(BrowserCookie.SUPPORT_BROWSER.keys()
                                                    ) + [str(i) for i in range(1, 11)]), callback=CLI.read_cookie, )
@option("--update_settings", "-us", type=bool,
        is_flag=True, )
@option("-h",
        is_flag=True,
        is_eager=True,
        expose_value=False,
        callback=CLI.help_, )
@option("--version", "-v",
        is_flag=True,
        is_eager=True,
        expose_value=False,
        callback=CLI.version, )
@pass_context
def cli(ctx, **kwargs):
    async def main():
        async with CLI(ctx, **kwargs) as xhs:
            await xhs.run()

    run(main())

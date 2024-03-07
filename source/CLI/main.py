from asyncio import run
from contextlib import suppress
from pathlib import Path as Root

from click import (
    command,
    option,
    Path,
    Choice,
    pass_context,
    Context,
    echo,
)

from source.application import XHS
from source.module import (
    ROOT,
    PROJECT,
)
from source.module import Settings
from .help import help

__all__ = ["cli"]


class CLI:
    def __init__(self, ctx: Context, **kwargs):
        self.ctx = ctx
        self.url = kwargs.pop("url")
        self.index = self.__format_index(kwargs.pop("index"))
        self.path = kwargs.pop("settings")
        self.update = kwargs.pop("update_settings")
        self.settings = Settings(self.__check_settings_path())
        self.parameter = self.settings.run() | self.__clean_params(kwargs)
        self.APP = XHS(**self.parameter)

    async def __aenter__(self):
        await self.APP.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.APP.__aexit__(exc_type, exc_value, traceback)

    async def run(self):
        if not self.url:
            echo("No URL specified")
            self.ctx.exit()
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
    def __clean_params(data: dict) -> dict:
        return {k: v for k, v in data.items() if v}

    def __check_params(self):
        pass

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
    def version(ctx: Context, *args, **kwargs):
        echo(PROJECT)
        ctx.exit()


@command(name="XHS-Downloader", help=PROJECT)
@option("--url", "-u", type=str, help="小红书作品链接", )
@option("--index", "-i", type=str, help="下载指定序号的图片文件，仅对图文作品生效", )
@option("--work_path",
        "-wp",
        type=Path(file_okay=False),
        help="作品数据 / 文件保存根路径",
        )
@option("--folder_name", "-fn", type=str, help="作品文件储存文件夹名称", )
@option("--user_agent", "-ua", type=str, help="请求头 User-Agent", )
@option("--cookie", "-ck", type=str, help="小红书网页版 Cookie，无需登录", )
@option("--proxy", "-p", type=str, help="设置程序代理", )
@option("--timeout", "-t", type=int, help="请求数据超时限制，单位：秒", )
@option("--chunk", "-c", type=int, help="下载文件时，每次从服务器获取的数据块大小，单位：字节", )
@option("--max_retry", "-mr", type=int, help="请求数据失败时，重试的最大次数，单位：秒", )
@option("--record_data", "-rd", type=bool, help="是否记录作品数据至 TXT 文件", )
@option("--image_format", "-if", type=Choice(["png", "PNG", "webp", "WEBP"]),
        help="图文作品文件下载格式，支持：PNG、WEBP", )
@option("--folder_mode", "-fm", type=bool, help="是否将每个作品的文件储存至单独的文件夹", )
@option("--language", "-l",
        type=Choice(["zh-CN", "en-GB"]), help="设置程序语言，目前支持：zh-CN、en-GB", )
@option("--settings", "-s", type=Path(dir_okay=False), help="读取指定配置文件", )
@option("--update_settings", "-us", type=bool, help="是否更新配置文件", )
@option("-h",
        is_flag=True,
        is_eager=True,
        expose_value=False,
        help="查看详细参数说明",
        callback=help)
@option("--version", "-v", is_flag=True, is_eager=True,
        expose_value=False, help="查看程序版本信息", callback=CLI.version)
@pass_context
def cli(ctx, **kwargs):
    async def main():
        async with CLI(ctx, **kwargs) as xhs:
            await xhs.run()

    run(main())

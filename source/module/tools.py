from asyncio import sleep
from random import uniform
from typing import Callable

from rich import print
from rich.text import Text

from ..translation import _
from .static import INFO


def retry(function):
    async def inner(self, *args, **kwargs):
        if result := await function(self, *args, **kwargs):
            return result
        for __ in range(self.retry):
            if result := await function(self, *args, **kwargs):
                return result
        return result

    return inner


def retry_limited(function):
    # TODO: 不支持 TUI
    def inner(self, *args, **kwargs):
        while True:
            if function(self, *args, **kwargs):
                return
            if self.console.input(
                _(
                    "如需重新尝试处理该对象，请关闭所有正在访问该对象的窗口或程序，然后直接按下回车键！\n"
                    "如需跳过处理该对象，请输入任意字符后按下回车键！"
                ),
            ):
                return

    return inner


def logging(log: Callable, text, style=INFO):
    string = Text(text, style=style)
    func = log()
    if func is print:
        func(string)
    else:
        func.write(
            string,
            scroll_end=True,
        )


async def sleep_time(
    min_time: int | float = 2.0,
    max_time: int | float = 4.0,
):
    await sleep(uniform(min_time, max_time))

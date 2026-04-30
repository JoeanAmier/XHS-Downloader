from asyncio import sleep
from random import lognormvariate
from math import log
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


def logging(log: Callable | None, text, style=INFO):
    if not log:
        return
    string = Text(text, style=style)
    func = log()
    if func is print:
        func(string)
    else:
        func.write(
            string,
            scroll_end=True,
        )


def get_wait_time(
    avg_delay: float | int = 6.0,
    sigma: float = 0.6,
) -> float:
    mu = log(avg_delay) - (sigma**2 / 2)
    return max(0.5, lognormvariate(mu, sigma))


async def sleep_time():
    await sleep(get_wait_time())

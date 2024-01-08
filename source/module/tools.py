from asyncio import sleep
from random import randint

from rich.text import Text

from .static import INFO

__all__ = ["retry", "logging", "wait"]


def retry(function):
    async def inner(self, *args, **kwargs):
        if result := await function(self, *args, **kwargs):
            return result
        for _ in range(self.retry):
            if result := await function(self, *args, **kwargs):
                return result
        return result

    return inner


def logging(log, text, style=INFO):
    string = Text(text, style=style)
    if log:
        log.write(string)
    else:
        print(string)


async def wait():
    await sleep(randint(15, 35) * 0.1)

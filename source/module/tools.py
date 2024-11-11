# from asyncio import sleep
# from random import uniform

from rich import print
from rich.text import Text

from .static import INFO


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


async def sleep_time(
        min_time: int | float = 1,
        max_time: int | float = 3,
):
    pass
    # await sleep(uniform(min_time, max_time))

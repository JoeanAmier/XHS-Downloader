from rich.text import Text

from .Static import INFO

__all__ = ["retry", "logging"]


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

from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import ServerDisconnectedError
from aiohttp import ServerTimeoutError

__all__ = ["Html", "retry"]


def retry(function):
    async def inner(self, *args, **kwargs):
        if result := await function(self, *args, **kwargs):
            return result
        for _ in range(self.retry):
            if result := await function(self, *args, **kwargs):
                return result
        return result

    return inner


class Html:

    def __init__(
            self,
            headers: dict,
            proxy: str = "",
            timeout=10,
            retry_=5, ):
        self.proxy = proxy
        self.session = ClientSession(
            headers=headers | {
                "Referer": "https://www.xiaohongshu.com/", },
            timeout=ClientTimeout(connect=timeout),
        )
        self.retry = retry_

    @retry
    async def request_url(
            self,
            url: str,
            text=True, ) -> str:
        try:
            async with self.session.get(
                    url,
                    proxy=self.proxy,
            ) as response:
                return await response.text() if text else str(response.url)
        except (
                ServerTimeoutError,
                ServerDisconnectedError,
        ):
            return ""

    @staticmethod
    def format_url(url: str) -> str:
        return bytes(url, "utf-8").decode("unicode_escape")

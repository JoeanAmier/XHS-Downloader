from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import ServerTimeoutError

__all__ = ['Html']


class Html:

    def __init__(
            self,
            headers: dict,
            proxy: str = None,
            timeout=10, ):
        self.proxy = proxy
        self.session = ClientSession(
            headers=headers | {
                "Referer": "https://www.xiaohongshu.com/", },
            timeout=ClientTimeout(connect=timeout),
        )

    async def request_url(
            self,
            url: str,
            text=True, ) -> str:
        try:
            async with self.session.get(
                    url,
                    proxy=self.proxy,
            ) as response:
                return await response.text() if text else response.url
        except ServerTimeoutError:
            return ""

    @staticmethod
    def format_url(url: str) -> str:
        return bytes(url, "utf-8").decode("unicode_escape")

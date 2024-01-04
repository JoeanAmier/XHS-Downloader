from aiohttp import ClientError

from .Manager import Manager
from .Static import ERROR
from .Tools import logging
from .Tools import retry

__all__ = ["Html"]


class Html:
    def __init__(self, manager: Manager, ):
        self.proxy = manager.proxy
        self.retry = manager.retry
        self.session = manager.request_session

    @retry
    async def request_url(
            self,
            url: str,
            content=True,
            log=None,
    ) -> str:
        try:
            async with self.session.get(
                    url,
                    proxy=self.proxy,
            ) as response:
                return await response.text() if content else str(response.url)
        except ClientError as error:
            logging(log, error, ERROR)
            logging(log, f"网络异常，请求 {url} 失败！", ERROR)
            return ""

    @staticmethod
    def format_url(url: str) -> str:
        return bytes(url, "utf-8").decode("unicode_escape")

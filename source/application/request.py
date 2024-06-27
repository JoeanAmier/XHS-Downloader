from httpx import HTTPError

from source.module import ERROR
from source.module import Manager
from source.module import logging
from source.module import retry

__all__ = ["Html"]


class Html:
    def __init__(self, manager: Manager, ):
        self.retry = manager.retry
        self.message = manager.message
        self.client = manager.request_client

    @retry
    async def request_url(
            self,
            url: str,
            content=True,
            log=None,
            **kwargs,
    ) -> str:
        try:
            response = await self.client.get(
                url,
                **kwargs,
            )
            if response.status_code != 200:
                return ""
            return response.text if content else str(response.url)
        except HTTPError as error:
            logging(log, str(error), ERROR)
            logging(
                log, self.message("网络异常，请求 {0} 失败").format(url), ERROR)
            return ""

    @staticmethod
    def format_url(url: str) -> str:
        return bytes(url, "utf-8").decode("unicode_escape")

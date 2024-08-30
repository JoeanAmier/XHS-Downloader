from httpx import HTTPError

from source.module import ERROR
from source.module import Manager
from source.module import logging
from source.module import retry
from source.module import sleep_time

__all__ = ["Html"]


class Html:
    def __init__(self, manager: Manager, ):
        self.retry = manager.retry
        self.message = manager.message
        self.client = manager.request_client
        self.headers = manager.headers
        self.blank_headers = manager.blank_headers

    @retry
    async def request_url(
            self,
            url: str,
            content=True,
            log=None,
            **kwargs,
    ) -> str:
        headers = self.select_headers(url, )
        try:
            match content:
                case True:
                    response = await self.__request_url_get(url, headers, **kwargs, )
                    await sleep_time()
                    response.raise_for_status()
                    return response.text
                case False:
                    response = await self.__request_url_head(url, headers, **kwargs, )
                    await sleep_time()
                    return str(response.url)
        except HTTPError as error:
            logging(
                log,
                self.message("网络异常，{0} 请求失败: {1}").format(url, repr(error)),
                ERROR
            )
            return ""

    @staticmethod
    def format_url(url: str) -> str:
        return bytes(url, "utf-8").decode("unicode_escape")

    def select_headers(self, url: str) -> dict:
        return self.headers if "explore" in url else self.blank_headers

    async def __request_url_head(self, url: str, headers: dict, **kwargs, ):
        return await self.client.head(
            url,
            headers=headers,
            **kwargs,
        )

    async def __request_url_get(self, url: str, headers: dict, **kwargs, ):
        return await self.client.get(
            url,
            headers=headers,
            **kwargs,
        )

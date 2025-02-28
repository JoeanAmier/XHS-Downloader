from httpx import HTTPError

from ..module import ERROR
from ..module import Manager
from ..module import logging
from ..module import retry
from ..module import sleep_time
from ..translation import _

__all__ = ["Html"]


class Html:
    def __init__(
            self,
            manager: Manager,
    ):
        self.retry = manager.retry
        self.client = manager.request_client
        self.headers = manager.headers

    @retry
    async def request_url(
            self,
            url: str,
            content=True,
            log=None,
            cookie: str = None,
            **kwargs,
    ) -> str:
        headers = self.update_cookie(
            cookie,
        )
        try:
            match content:
                case True:
                    response = await self.__request_url_get(
                        url,
                        headers,
                        **kwargs,
                    )
                    await sleep_time()
                    response.raise_for_status()
                    return response.text
                case False:
                    response = await self.__request_url_head(
                        url,
                        headers,
                        **kwargs,
                    )
                    await sleep_time()
                    return str(response.url)
                case _:
                    raise ValueError
        except HTTPError as error:
            logging(
                log, _("网络异常，{0} 请求失败: {1}").format(url, repr(error)), ERROR
            )
            return ""

    @staticmethod
    def format_url(url: str) -> str:
        return bytes(url, "utf-8").decode("unicode_escape")

    def update_cookie(
            self,
            cookie: str = None,
    ) -> dict:
        return self.headers | {"Cookie": cookie} if cookie else self.headers.copy()

    async def __request_url_head(
            self,
            url: str,
            headers: dict,
            **kwargs,
    ):
        return await self.client.head(
            url,
            headers=headers,
            **kwargs,
        )

    async def __request_url_get(
            self,
            url: str,
            headers: dict,
            **kwargs,
    ):
        return await self.client.get(
            url,
            headers=headers,
            **kwargs,
        )

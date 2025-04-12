from typing import TYPE_CHECKING

from httpx import HTTPError
from httpx import get

from ..module import ERROR, Manager, logging, retry, sleep_time
from ..translation import _

if TYPE_CHECKING:
    from ..module import Manager

__all__ = ["Html"]


class Html:
    def __init__(
        self,
        manager: "Manager",
    ):
        self.retry = manager.retry
        self.client = manager.request_client
        self.headers = manager.headers
        self.timeout = manager.timeout

    @retry
    async def request_url(
        self,
        url: str,
        content=True,
        log=None,
        cookie: str = None,
        proxy: str = None,
        **kwargs,
    ) -> str:
        headers = self.update_cookie(
            cookie,
        )
        try:
            match (content, bool(proxy)):
                case (True, False):
                    response = await self.__request_url_get(
                        url,
                        headers,
                        **kwargs,
                    )
                    await sleep_time()
                    response.raise_for_status()
                    return response.text
                case (True, True):
                    response = await self.__request_url_get_proxy(
                        url,
                        headers,
                        proxy,
                        **kwargs,
                    )
                    await sleep_time()
                    response.raise_for_status()
                    return response.text
                case (False, False):
                    response = await self.__request_url_head(
                        url,
                        headers,
                        **kwargs,
                    )
                    await sleep_time()
                    return str(response.url)
                case (False, True):
                    response = await self.__request_url_head_proxy(
                        url,
                        headers,
                        proxy,
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

    async def __request_url_head_proxy(
        self,
        url: str,
        headers: dict,
        proxy: str,
        **kwargs,
    ):
        return await self.client.head(
            url,
            headers=headers,
            proxy=proxy,
            follow_redirects=True,
            verify=False,
            timeout=self.timeout,
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

    async def __request_url_get_proxy(
        self,
        url: str,
        headers: dict,
        proxy: str,
        **kwargs,
    ):
        return get(
            url,
            headers=headers,
            proxy=proxy,
            follow_redirects=True,
            verify=False,
            timeout=self.timeout,
            **kwargs,
        )

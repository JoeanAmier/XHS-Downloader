from typing import TYPE_CHECKING

from curl_cffi.requests.exceptions import RequestException

from ..module import ERROR, logging, retry, sleep_time
from ..translation import _

if TYPE_CHECKING:
    from ..module import Manager

__all__ = ["Html"]


class Html:
    def __init__(
        self,
        manager: "Manager",
    ):
        self.manager = manager
        self.print = manager.print
        self.retry = manager.retry
        self.client = manager.request_client
        self.timeout = manager.timeout
        self.proxy = manager.proxy
        self.impersonate = manager.impersonate
        # 记录上次使用的 Cookie，重试时优先切换到下一个。
        self._last_cookie: str | None = None

    @retry
    async def request_url(
        self,
        url: str,
        content=True,
        cookie: str | None = None,
        proxy: str | None = None,
        **kwargs,
    ) -> str:
        if not url.startswith("http"):
            url = f"https://{url}"
        headers = self.manager.get_headers(url)
        # 多 Cookie 支持：显式传入优先，否则从 Cookie 池轮流挑选（避开上次失败的）。
        use_cookie = cookie if cookie else self.manager.pick_cookie(
            exclude=self._last_cookie
        )
        self._last_cookie = use_cookie
        if use_cookie:
            # 通过 header 精确指定 Cookie，避免与会话 cookie jar 合并冲突。
            headers["cookie"] = use_cookie
        try:
            response = await self.__request_url_get(
                url,
                headers,
                proxy=proxy,
                **kwargs,
            )
            await sleep_time()
            response.raise_for_status()
            return response.text if content else str(response.url)
        except RequestException as error:
            logging(
                self.print,
                _("网络异常，{0} 请求失败: {1}").format(url, repr(error)),
                ERROR,
            )
            return ""

    @staticmethod
    def format_url(url: str) -> str:
        return bytes(url, "utf-8").decode("unicode_escape")

    async def __request_url_get(
        self,
        url: str,
        headers: dict,
        proxy: str | None = None,
        **kwargs,
    ):
        return await self.client.get(
            url,
            headers=headers,
            proxy=self.proxy if proxy is None else proxy,
            **kwargs,
        )

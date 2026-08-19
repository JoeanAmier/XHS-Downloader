from typing import TYPE_CHECKING

from xhshow import Xhshow

from ..module import retry, sleep_time

if TYPE_CHECKING:
    from ..module import Manager


class UserPosted:
    encipher = Xhshow()

    def __init__(
        self,
        manager: "Manager",
        url: str,
        params: dict,
        cookies: str | None = None,
        proxy: str | None = None,
    ):
        self.url = url
        self.params = params
        self.headers = manager.blank_headers.copy()
        self.client = manager.request_client
        self.cookies = self.get_cookie(cookies)
        self.print = manager.print
        self.retry = manager.retry
        self.proxy = (self.client.proxies.get("all", None) if proxy is None else proxy,)

    def get_cookie(self, cookies: str | None = None) -> dict | str:
        if cookies:
            self.headers["cookie"] = cookies
            return cookies
        return dict(self.client.cookies)

    def run(
        self,
        verify=True,
    ): ...

    @retry
    async def get_data(self):
        headers = self.get_headers()
        response = await self.client.get(
            self.url,
            params=self.params,
            headers=headers,
            proxy=self.proxy,
        )
        await sleep_time()
        response.raise_for_status()
        return response.json()

    def get_headers(self):
        headers = self.encipher.sign_headers_get(
            uri=self.url,
            cookies=self.cookies,
            params=self.params,
        )
        return headers | self.headers

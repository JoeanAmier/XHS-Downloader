from xhshow import Xhshow
from typing import TYPE_CHECKING
from ..module import retry, sleep_time
from httpx import get

if TYPE_CHECKING:
    from ..module import Manager


class UserPosted:
    encipher = Xhshow()

    def __init__(
        self,
        manager: "Manager",
        url: str,
        params: dict,
        cookies: str = None,
        proxy: str = None,
    ):
        self.url = url
        self.params = params
        self.headers = manager.blank_headers.copy()
        self.client = manager.request_client
        self.cookies = self.get_cookie(cookies)
        self.print = manager.print
        self.retry = manager.retry
        self.timeout = manager.timeout
        self.proxy = proxy

    def get_cookie(self, cookies: str = None) -> dict | str:
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
        if self.proxy:
            response = get(
                self.url,
                params=self.params,
                headers=headers,
                proxy=self.proxy,
                follow_redirects=True,
                verify=False,
                timeout=self.timeout,
            )
        else:
            response = await self.client.get(
                self.url,
                params=self.params,
                headers=headers,
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

from requests import exceptions
from requests import get

__all__ = ['Html']


class Html:

    def __init__(
            self,
            headers: dict,
            proxies=None,
            timeout=10, ):
        self.headers = headers | {"Referer": "https://www.xiaohongshu.com/", }
        self.proxies = {
            "http": proxies,
            "https": proxies,
            "ftp": proxies,
        }
        self.timeout = timeout

    def request_url(
            self,
            url: str,
            params=None,
            headers=None,
            text=True, ) -> str:
        try:
            response = get(
                url,
                params=params,
                proxies=self.proxies,
                timeout=self.timeout,
                headers=headers or self.headers, )
        except (
                exceptions.ProxyError,
                exceptions.SSLError,
                exceptions.ChunkedEncodingError,
                exceptions.ConnectionError,
                exceptions.ReadTimeout,
        ):
            print("网络异常，获取网页源码失败！")
            return ""
        return response.text if text else response.url

    @staticmethod
    def format_url(url: str) -> str:
        return bytes(url, "utf-8").decode("unicode_escape")

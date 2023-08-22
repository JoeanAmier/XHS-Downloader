import requests
from requests import get


class Html:

    def __init__(
            self,
            headers: dict,
            proxies=None,
            timeout=10, ):
        self.headers = headers
        self.proxies = {
            "http": proxies,
            "https": proxies,
            "ftp": proxies,
        }
        self.timeout = timeout

    def get_html(
            self,
            url: str,
            params=None,
            headers=None,
            allow_redirects=True) -> str:
        try:
            response = get(
                url,
                params=params,
                proxies=self.proxies,
                timeout=self.timeout,
                headers=headers or self.headers,
                allow_redirects=allow_redirects, )
        except (
                requests.exceptions.ProxyError,
                requests.exceptions.SSLError,
                requests.exceptions.ChunkedEncodingError,
                requests.exceptions.ConnectionError,
                requests.ReadTimeout,
        ):
            return ""
        return response.text

import requests
from requests import get


class Html:

    def __init__(self, headers: dict):
        self.headers = headers

    def get_html(
            self,
            url: str,
            params=None,
            proxies=None,
            timeout=10,
            **kwargs) -> str:
        try:
            response = get(
                url,
                params=params,
                proxies=proxies,
                timeout=timeout,
                headers=self.headers,
                **kwargs)
        except (
                requests.exceptions.ProxyError,
                requests.exceptions.SSLError,
                requests.exceptions.ChunkedEncodingError,
                requests.exceptions.ConnectionError,
                requests.ReadTimeout,
        ):
            return ""
        return response.text

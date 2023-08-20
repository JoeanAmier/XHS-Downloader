import requests


class Html:

    def __init__(self, headers: dict):
        self.headers = headers

    def get_html(
            self,
            url: str,
            params=None,
            proxies=None,
            timeout=10,
            **kwargs):
        response = requests.get(
            url,
            params=params,
            proxies=proxies,
            timeout=timeout,
            headers=self.headers,
            **kwargs)
        return response.text

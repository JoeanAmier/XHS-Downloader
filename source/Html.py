import requests

from .Params import HEADERS


def get_html(
        url,
        cookie=None,
        params=None,
        proxies=None,
        timeout=10,
        **kwargs):
    if cookie:
        update_cookie(cookie)
    response = requests.get(
        url,
        params=params,
        proxies=proxies,
        timeout=timeout,
        headers=HEADERS,
        **kwargs)
    return response.text


def update_cookie(cookie: str):
    HEADERS["Cookie"] = cookie

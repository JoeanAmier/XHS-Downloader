# from .Params import HEADERS
from .Params import API
from .Params import ID


def get_id(html: str):
    return ID.findall(html)


def generate_url(ids: list):
    return [API + i for i in ids]


def download(url, path):
    pass

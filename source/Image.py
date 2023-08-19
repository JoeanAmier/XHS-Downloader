# from .Params import HEADERS
from .Params import ID
from .Params import IMAGE_API


def get_id(html: str):
    return ID.findall(html)


def generate_url(ids: list):
    return [IMAGE_API + i for i in ids]


def download(url, path):
    pass

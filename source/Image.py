from .Params import ID
from .Params import IMAGE_API


def get_id(html: str) -> list:
    return ID.findall(html)


def generate_url(ids: list) -> list:
    return [IMAGE_API + i for i in ids]


def get_url(html: str) -> list:
    return generate_url(get_id(html))

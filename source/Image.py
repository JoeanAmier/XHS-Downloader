import re

API = "https://sns-img-qc.xhscdn.com/"
ID = re.compile(r'"traceId":"(.*?)"')


def get_id(html: str):
    return ID.findall(html)


def generate_url(ids: list):
    return [API + i for i in ids]

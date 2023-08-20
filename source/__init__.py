from .Html import get_html
from .Image import get_url
from .Params import Params


class XHS:
    def __init__(self, path="./"):
        self.params = Params(path)
        self.image = Image(self.params)

    def get_image(self, url: str, cookie=None, ):
        return self.image.get_image_link(url, cookie)


class Image:
    def __init__(self, params):
        self.params = params

    @staticmethod
    def get_image_link(url: str, cookie=None, ):
        html = get_html(url, cookie=cookie, )
        return get_url(html)

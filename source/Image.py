from re import compile

from .Html import Html

__all__ = ['Image']


class Image:
    IMAGE_URL = compile(r'"CRD_WM_.*?","url":"(.*?)"')

    def get_image_link(self, html: str) -> list:
        return [Html.format_url(i) for i in self.IMAGE_URL.findall(html)]

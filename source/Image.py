from re import compile

from .Html import Html

__all__ = ['Image']


class Image:
    IMAGE_TOKEN = compile(
        r'"urlDefault":"http:\\u002F\\u002Fsns-webpic-qc\.xhscdn\.com\\u002F\d+?\\u002F\S+?\\u002F(\S+?)!')

    def get_image_link(self, html: str) -> list:
        return [Html.format_url(self.__generate_image_link(i))
                for i in self.IMAGE_TOKEN.findall(html)]

    @staticmethod
    def __generate_image_link(token: str) -> str:
        return f"https://sns-img-bd.xhscdn.com/{token}"

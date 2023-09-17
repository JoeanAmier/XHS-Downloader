from json import loads
from re import compile

from .Html import Html

__all__ = ['Image']


class Image:
    IMAGE_INFO = compile(r'("infoList":\[\{.*?}])')

    def get_image_link(self, html: str) -> list:
        data = self.__extract_image_data(html)
        data = self.__format_image_data(data)
        return self.__extract_image_urls(data)

    def __extract_image_data(self, html: str) -> list[str]:
        return self.IMAGE_INFO.findall(html)

    @staticmethod
    def __format_image_data(data: list[str]) -> list[dict]:
        return [loads(f"{{{i}}}") for i in data]

    @staticmethod
    def __extract_image_urls(data: list[dict]) -> list[str]:
        urls = []
        for i in data:
            for j in i.get("infoList", []):
                if j.get("imageScene", "").startswith("CRD_WM_"):
                    urls.append(j.get("url", ""))
                    break
        return [Html.format_url(i) for i in urls if i]

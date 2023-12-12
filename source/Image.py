from json import loads
from re import compile

__all__ = ['Image']


class Image:
    IMAGE_INFO = compile(r'("infoList":\[\{.*?}])')
    IMAGE_TOKEN = compile(
        r"http://sns-webpic-qc.xhscdn.com/\d+/\w+/(\w+)!")

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
    def __generate_image_link(token: str) -> str:
        return f"https://sns-img-bd.xhscdn.com/{token}"

    def __extract_image_token(self, url: str) -> str:
        return self.__generate_image_link(token.group(1)) if (
            token := self.IMAGE_TOKEN.search(url)) else ""

    def __extract_image_urls(self, data: list[dict]) -> list[str]:
        urls = []
        for i in data:
            for j in i.get("infoList", []):
                if j.get("imageScene", "") == "WB_DFT":
                    urls.append(self.__extract_image_token(j.get("url", "")))
                    break
        return [i for i in urls if i]

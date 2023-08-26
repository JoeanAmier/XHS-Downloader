from re import compile


class Image:
    IMAGE_API = "https://sns-img-qc.xhscdn.com/"
    IMAGE_ID = compile(r'"traceId":"(.*?)"')

    def __init__(self, html: str):
        self.html = html

    def get_image_link(self, url: str, download: bool):
        html = self.html.get_html(url)
        return self.__get_image_links(html)

    def __get_id(self, html: str) -> list:
        return self.IMAGE_ID.findall(html)

    def __generate_url(self, ids: list) -> list:
        return [self.IMAGE_API + i for i in ids]

    def __get_image_links(self, html: str) -> list:
        return self.__generate_url(self.__get_id(html))

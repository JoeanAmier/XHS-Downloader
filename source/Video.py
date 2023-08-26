from re import compile


class Video:
    VIDEO_ID = compile(r'"masterUrl":"(.*?)"')

    def __init__(self, html):
        self.html = html

    def get_video_link(self, url: str, download: bool):
        html = self.html.get_html(url)
        return self.__get_video_link(html)

    def __get_video_link(self, html: str) -> list:
        return [self.clean_url(u) for u in self.VIDEO_ID.findall(html)]

    @staticmethod
    def clean_url(url: str) -> str:
        return bytes(url, "utf-8").decode("unicode_escape")

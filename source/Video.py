from re import compile

from .Html import Html

__all__ = ['Video']


class Video:
    VIDEO_ID = compile(r'"masterUrl":"(.*?)"')

    def get_video_link(self, html: str):
        return [Html.format_url(u) for u in self.VIDEO_ID.findall(html)]

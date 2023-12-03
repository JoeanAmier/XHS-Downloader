from re import compile

from .Html import Html

__all__ = ['Video']


class Video:
    VIDEO_TOKEN = compile(r'"originVideoKey":"(\S+?\\u002F\S+?)"')

    def get_video_link(self, html: str) -> list:
        return [Html.format_url(f"https://sns-video-hw.xhscdn.com/{
        t.group(1)}")] if (t := self.VIDEO_TOKEN.search(html)) else []

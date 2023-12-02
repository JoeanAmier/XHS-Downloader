from re import compile

__all__ = ['Video']


class Video:
    VIDEO_TOKEN = compile(r'"originVideoKey":"pre_post\\u002F(\S+?)"')

    def get_video_link(self, html: str) -> list:
        return [f"https://sns-video-hw.xhscdn.com/pre_post/{
        t.group(1)}"] if (t := self.VIDEO_TOKEN.search(html)) else []

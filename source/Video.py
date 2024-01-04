from .Converter import Namespace
from .Html import Html

__all__ = ['Video']


class Video:
    VIDEO_LINK = (
        "video",
        "consumer",
        "originVideoKey",
    )

    @classmethod
    def get_video_link(cls, data: Namespace) -> list:
        return [Html.format_url(f"https://sns-video-hw.xhscdn.com/{t}")] if (
            t := data.safe_extract(".".join(cls.VIDEO_LINK))) else []

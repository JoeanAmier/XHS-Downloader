from source.expansion import Namespace
from .request import Html

__all__ = ["Video"]


class Video:
    VIDEO_LINK = (
        "video",
        "consumer",
        "originVideoKey",
    )

    @classmethod
    def deal_video_link(
        cls,
        data: Namespace,
        preference="resolution",
    ):
        return cls.generate_video_link(data) or cls.get_video_link(data, preference)

    @classmethod
    def generate_video_link(cls, data: Namespace) -> list:
        return (
            [Html.format_url(f"https://sns-video-bd.xhscdn.com/{t}")]
            if (t := data.safe_extract(".".join(cls.VIDEO_LINK)))
            else []
        )

    @classmethod
    def get_video_link(
        cls,
        data: Namespace,
        preference="resolution",
    ) -> list:
        if not (items := cls.get_video_items(data)):
            return []
        match preference:
            case "resolution":
                items.sort(key=lambda x: x.height)
            case "bitrate":
                items.sort(key=lambda x: x.videoBitrate)
            case "size":
                items.sort(key=lambda x: x.size)
            case _:
                raise ValueError(f"Invalid video preference value: {preference}")
        return [b[0]] if (b := items[-1].backupUrls) else [items[-1].masterUrl]

    @staticmethod
    def get_video_items(data: Namespace) -> list:
        keys = data.safe_extract("video.media.stream").__dict__.keys()
        items = []
        for key in keys:
            item = data.safe_extract(f"video.media.stream.{key}", [])
            items.extend(item)
        return items

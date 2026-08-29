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

    @staticmethod
    def is_h264(item: Namespace) -> bool:
        codec = str(getattr(item, "videoCodec", "")).lower()
        desc = str(getattr(item, "streamDesc", "")).lower()
        try:
            stream_type = int(getattr(item, "streamType", 0))
        except (TypeError, ValueError):
            stream_type = 0
        # 小红书登录页面返回的流使用 EF4/EF5 这类编码标识。
        # EF4 对应 H.264/AVC，EF5 对应 H.265/HEVC；streamType 258/259 等小于 300 的也属于 AVC。
        return (
            codec in {"h264", "avc1", "x264", "ef4"}
            or "x264" in desc
            or 0 < stream_type < 300
        )

    @classmethod
    def get_video_link(
        cls,
        data: Namespace,
        preference="resolution",
    ) -> list:
        if not (items := cls.get_video_items(data)):
            return []
        # Prefer H.264/AVC to avoid HEVC playback issues (audio only).
        if compatible := [item for item in items if cls.is_h264(item)]:
            items = compatible
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

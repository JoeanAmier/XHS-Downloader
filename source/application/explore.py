from datetime import datetime

from ..expansion import Namespace
from ..translation import _

__all__ = ["Explore"]


class Explore:
    time_format = "%Y-%m-%d_%H:%M:%S"

    def __init__(self):
        self.explore_type = {"video": _("视频"), "normal": _("图文")}

    def run(self, data: Namespace) -> dict:
        return self.__extract_data(data)

    def __extract_data(self, data: Namespace) -> dict:
        result = {}
        if data:
            self.__extract_interact_info(result, data)
            self.__extract_tags(result, data)
            self.__extract_info(result, data)
            self.__extract_time(result, data)
            self.__extract_user(result, data)
        return result

    @staticmethod
    def __extract_interact_info(container: dict, data: Namespace) -> None:
        container["收藏数量"] = data.safe_extract("interactInfo.collectedCount", "-1")
        container["评论数量"] = data.safe_extract("interactInfo.commentCount", "-1")
        container["分享数量"] = data.safe_extract("interactInfo.shareCount", "-1")
        container["点赞数量"] = data.safe_extract("interactInfo.likedCount", "-1")

    @staticmethod
    def __extract_tags(container: dict, data: Namespace):
        tags = data.safe_extract("tagList", [])
        container["作品标签"] = " ".join(
            Namespace.object_extract(i, "name") for i in tags
        )

    def __extract_info(self, container: dict, data: Namespace):
        container["作品ID"] = data.safe_extract("noteId")
        container["作品链接"] = (
            f"https://www.xiaohongshu.com/explore/{container['作品ID']}"
        )
        container["作品标题"] = data.safe_extract("title")
        container["作品描述"] = data.safe_extract("desc")
        container["作品类型"] = self.explore_type.get(
            data.safe_extract("type"), _("未知")
        )
        # container["IP归属地"] = data.safe_extract("ipLocation")

    def __extract_time(self, container: dict, data: Namespace):
        container["发布时间"] = (
            datetime.fromtimestamp(time / 1000).strftime(self.time_format)
            if (time := data.safe_extract("time"))
            else _("未知")
        )
        container["最后更新时间"] = (
            datetime.fromtimestamp(last / 1000).strftime(self.time_format)
            if (last := data.safe_extract("lastUpdateTime"))
            else _("未知")
        )
        container["时间戳"] = (
            (time / 1000) if (time := data.safe_extract("time")) else None
        )

    @staticmethod
    def __extract_user(container: dict, data: Namespace):
        container["作者昵称"] = data.safe_extract("user.nickname")
        container["作者ID"] = data.safe_extract("user.userId")
        container["作者链接"] = (
            f"https://www.xiaohongshu.com/user/profile/{container['作者ID']}"
        )

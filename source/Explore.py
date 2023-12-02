from datetime import datetime
from json import loads
from re import compile

__all__ = ['Explore']


class Explore:
    explore_data = compile(
        r'"currentTime":\d{13},"note":(.*?)}},"serverRequestInfo"')
    time_format = "%Y-%m-%d %H:%M:%S"

    def run(self, html: str) -> dict:
        data = self.__get_json_data(html)
        return self.__extract_data(data)

    def __get_json_data(self, html: str) -> dict:
        data = self.explore_data.search(html)
        return loads(data.group(1)) if data else {}

    def __extract_data(self, data: dict) -> dict:
        result = {}
        if data:
            self.__extract_interact_info(result, data)
            self.__extract_tags(result, data)
            self.__extract_info(result, data)
            self.__extract_time(result, data)
            self.__extract_user(result, data)
        return result

    @staticmethod
    def __extract_interact_info(container: dict, data: dict):
        interact_info = data.get("interactInfo", {})
        container["收藏数量"] = interact_info.get("collectedCount")
        container["评论数量"] = interact_info.get("commentCount")
        container["分享数量"] = interact_info.get("shareCount")
        container["点赞数量"] = interact_info.get("likedCount")

    @staticmethod
    def __extract_tags(container: dict, data: dict):
        tags = data.get("tagList", [])
        container["作品标签"] = [i.get("name", "") for i in tags]

    @staticmethod
    def __extract_info(container: dict, data: dict):
        container["作品ID"] = data.get("noteId")
        container["作品标题"] = data.get("title")
        container["作品描述"] = data.get("desc")
        container["作品类型"] = {
            "video": "视频", "normal": "图文"}.get(
            data.get("type"), "未知")
        container["IP归属地"] = data.get("ipLocation")

    def __extract_time(self, container: dict, data: dict):
        container["发布时间"] = datetime.fromtimestamp(
            time /
            1000).strftime(
            self.time_format) if (
            time := data.get("time")) else "未知"
        container["最后更新时间"] = datetime.fromtimestamp(
            last /
            1000).strftime(
            self.time_format) if (last := data.get("lastUpdateTime")) else "未知"

    @staticmethod
    def __extract_user(container: dict, data: dict):
        user = data.get("user", {})
        container["作者昵称"] = user.get("nickname")
        container["作者ID"] = user.get("userId")

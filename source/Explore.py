from json import loads
from re import compile
from time import strftime


class Explore:
    explore_data = compile(
        r'"currentTime":\d{13},"note":(.*?)}},"serverRequestInfo"')
    time_format = "%Y-%m-%d %H:%M:%S"

    def run(self, html: str) -> dict:
        data = self.__get_json_data(html)
        return self.__extract_data(data)

    def __get_json_data(self, html: str) -> dict:
        data = self.explore_data.findall(html)
        return {} if len(data) != 1 else loads(data[0])

    def __extract_data(self, data: dict) -> dict:
        result = {}
        self.__extract_interact_info(result, data)
        self.__extract_tags(result, data)
        self.__extract_info(result, data)
        self.__extract_time(result, data)
        self.__extract_user(result, data)
        return result

    @staticmethod
    def __extract_interact_info(container: dict, data: dict):
        interact_info = data["interactInfo"]
        container["收藏数量"] = interact_info["collectedCount"]
        container["评论数量"] = interact_info["commentCount"]
        container["分享数量"] = interact_info["shareCount"]
        container["点赞数量"] = interact_info["likedCount"]

    @staticmethod
    def __extract_tags(container: dict, data: dict):
        tags = data["tagList"]
        container["作品标签"] = [i["name"] for i in tags]

    @staticmethod
    def __extract_info(container: dict, data: dict):
        container["作品ID"] = data["noteId"]
        container["作品标题"] = data["title"]
        container["作品描述"] = data["desc"]
        container["作品类型"] = {"video": "视频", "normal": "图文"}[data["type"]]

    def __extract_time(self, container: dict, data: dict):
        container["发布时间"] = strftime(self.time_format, data["time"])
        container["最后更新时间"] = strftime(
            self.time_format, data["lastUpdateTime"])

    @staticmethod
    def __extract_user(container: dict, data: dict):
        user = data["user"]
        container["作者昵称"] = user["nickname"]
        container["作者ID"] = user["userId"]

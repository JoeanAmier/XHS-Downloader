from pathlib import Path
from shutil import move
from shutil import rmtree

__all__ = ["Manager"]


class Manager:
    def __init__(self, root: Path, ua: str, cookie: str, retry: int):
        self.temp = root.joinpath("./temp")
        self.headers = {
            "User-Agent": ua or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "Cookie": cookie or "abRequestId=54c534bb-a2c6-558f-8e03-5b4c5c45635c; xsecappid=xhs-pc-web; a1=18c286a400"
                                "4jy56qvzejvp631col0hd3032h4zjez50000106381; webId=779c977da3a15b5623015be94bdcc9e9; g"
                                "id=yYSJYK0qDW8KyYSJYK048quV84Vv2KAhudVhJduUKqySlx2818xfq4888y8KqYy8y2y2f8Jy; web_sess"
                                "ion=030037a259ce5f15c8d560dc12224a9fdc2ed1; webBuild=3.19.4; websectiga=984412fef754c"
                                "018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; sec_poison_id=3dd48845-d604-4535"
                                "-bcc2-a859e97518bf; unread={%22ub%22:%22655eb3d60000000032033955%22%2C%22ue%22:%22656"
                                "e9ef2000000003801ff3d%22%2C%22uc%22:29}; cache_feeds=[]"}
        self.retry = retry

    @staticmethod
    def is_exists(path: Path) -> bool:
        return path.exists()

    @staticmethod
    def delete(path: Path):
        path.unlink()

    @staticmethod
    def move(temp: Path, path: Path):
        move(temp.resolve(), path.resolve())

    def clean(self):
        rmtree(self.temp.resolve())

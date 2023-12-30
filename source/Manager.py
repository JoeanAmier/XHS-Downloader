from datetime import datetime
from json import dumps
from pathlib import Path
from re import compile
from re import sub
from shutil import move
from shutil import rmtree

__all__ = ["Manager"]


class Manager:
    NAME = compile(r"[^\u4e00-\u9fa5a-zA-Z0-9_]")

    def __init__(
            self,
            root: Path,
            path: str,
            folder: str,
            user_agent: str,
            chunk: int,
            cookie: str,
            proxy: str,
            timeout: int,
            retry: int,
            record_data: bool,
            image_format: str,
            video_format: str,
            folder_mode: bool,
    ):
        self.root = root
        self.temp = root.joinpath("./temp")
        self.folder = self.__init_root(root, path, folder)
        self.headers = {
            "User-Agent": user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gec"
                                        "ko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": cookie or "abRequestId=54c534bb-a2c6-558f-8e03-5b4c5c45635c; xsecappid=xhs-pc-web; a1=18c286a400"
                                "4jy56qvzejvp631col0hd3032h4zjez50000106381; webId=779c977da3a15b5623015be94bdcc9e9; g"
                                "id=yYSJYK0qDW8KyYSJYK048quV84Vv2KAhudVhJduUKqySlx2818xfq4888y8KqYy8y2y2f8Jy; web_sess"
                                "ion=030037a259ce5f15c8d560dc12224a9fdc2ed1; webBuild=3.19.4; websectiga=984412fef754c"
                                "018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; sec_poison_id=3dd48845-d604-4535"
                                "-bcc2-a859e97518bf; unread={%22ub%22:%22655eb3d60000000032033955%22%2C%22ue%22:%22656"
                                "e9ef2000000003801ff3d%22%2C%22uc%22:29}; cache_feeds=[]"}
        self.retry = retry
        self.chunk = chunk
        self.record_data = record_data
        self.image_format = image_format
        self.video_format = video_format
        self.folder_mode = folder_mode
        self.timeout = timeout
        self.proxy = proxy

    def __init_root(self, root: Path, path: str, folder: str) -> Path:
        if path and (r := Path(path)).is_dir():
            root = r.joinpath(folder or "Download")
        else:
            root = root.joinpath(folder or "Download")
        root.mkdir(exist_ok=True)
        self.temp.mkdir(exist_ok=True)
        return root

    @staticmethod
    def is_exists(path: Path) -> bool:
        return path.exists()

    @staticmethod
    def delete(path: Path):
        path.unlink()

    @staticmethod
    def archive(root: Path, name: str, folder_mode: bool) -> Path:
        return root.joinpath(name) if folder_mode else root

    @staticmethod
    def move(temp: Path, path: Path):
        move(temp.resolve(), path.resolve())

    def clean(self):
        rmtree(self.temp.resolve())

    def filter_name(self, name: str) -> str:
        name = self.NAME.sub("_", name)
        return sub(r"_+", "_", name).strip("_")

    def save_data(self, name: str, data: dict):
        if not self.record_data:
            return
        with self.folder.joinpath(f"{name}.txt").open("a", encoding="utf-8") as f:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = f"{time.center(50, '=')}\n{dumps(data, indent=4, ensure_ascii=False)}\n"
            f.write(content)

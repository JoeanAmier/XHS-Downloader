from pathlib import Path

from requests import exceptions
from requests import get


class Download:
    chunk = 262144

    def __init__(
            self,
            path,
            folder,
            headers: dict,
            proxies=None, ):
        self.root = self.init_root(path, folder)
        self.headers = self.init_headers(headers)
        self.proxies = {
            "http": proxies,
            "https": proxies,
            "ftp": proxies,
        }

    @staticmethod
    def init_headers(headers: dict) -> dict:
        return {"User-Agent": headers["User-Agent"]}

    @staticmethod
    def init_root(path: str, folder: str) -> Path:
        root = Path(path).joinpath(folder)
        if not root.is_dir():
            root.mkdir()
        return root

    def run(self, urls: list, name: str):
        if (l := len(urls)) > 1:
            for index, url in enumerate(urls):
                self.download(url, f"{name}_{index + 1}.webp")
        elif l == 1:
            self.download(urls[0], f"{name}.mp4")

    def download(self, url: str, name: str):
        try:
            with get(url, headers=self.headers, proxies=self.proxies, stream=True) as response:
                with self.root.joinpath(name).open("wb") as f:
                    for chunk in response.iter_content(chunk_size=self.chunk):
                        f.write(chunk)
            print(f"{name} 下载成功！")
        except exceptions.ChunkedEncodingError:
            print("网络异常，下载文件失败！")

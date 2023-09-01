from pathlib import Path

from requests import exceptions
from requests import get

__all__ = ['Download']


class Download:

    def __init__(
            self,
            manager,
            path,
            folder,
            headers: dict,
            proxies=None,
            chunk=256 * 1024, ):
        self.manager = manager
        self.root = self.init_root(path, folder)
        self.headers = headers
        self.proxies = {
            "http": proxies,
            "https": proxies,
            "ftp": proxies,
        }
        self.chunk = chunk

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
            print(f"网络异常，{name} 下载失败！")

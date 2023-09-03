from pathlib import Path

from requests import exceptions
from requests import get

from .Manager import Manager

__all__ = ['Download']


class Download:
    manager = Manager()
    temp = Path("./Temp")

    def __init__(
            self,
            path: str,
            folder: str,
            headers: dict,
            proxies=None,
            chunk=256 * 1024, ):
        self.root = self.init_root(path, folder)
        self.headers = headers
        self.proxies = {
            "http": proxies,
            "https": proxies,
            "ftp": proxies,
        }
        self.chunk = chunk

    def init_root(self, path: str, folder: str) -> Path:
        root = Path(path).joinpath(folder)
        if not root.is_dir():
            root.mkdir()
        if not self.temp.is_dir():
            self.temp.mkdir()
        return root

    def run(self, urls: list, name: str):
        if (l := len(urls)) > 1:
            for index, url in enumerate(urls):
                self.download(url, f"{name}_{index + 1}.webp")
        elif l == 1:
            self.download(urls[0], f"{name}.mp4")

    def download(self, url: str, name: str):
        temp = self.temp.joinpath(name)
        file = self.root.joinpath(name)
        if self.manager.is_exists(file):
            print(f"{name} 已存在，跳过下载！")
            return
        try:
            with get(url, headers=self.headers, proxies=self.proxies, stream=True) as response:
                with temp.open("wb") as f:
                    for chunk in response.iter_content(chunk_size=self.chunk):
                        f.write(chunk)
            self.manager.move(temp, file)
            print(f"{name} 下载成功！")
        except exceptions.ChunkedEncodingError:
            self.manager.delete(temp)
            print(f"网络异常，{name} 下载失败！")

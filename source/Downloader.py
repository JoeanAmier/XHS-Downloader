from pathlib import Path

from requests import exceptions
from requests import get

__all__ = ['Download']


class Download:

    def __init__(
            self,
            manager,
            root: Path,
            path: str,
            folder: str,
            proxies=None,
            chunk=1024 * 1024,
            timeout=10, ):
        self.manager = manager
        self.temp = manager.temp
        self.headers = manager.headers
        self.root = self.__init_root(root, path, folder)
        self.proxies = {
            "http": proxies,
            "https": proxies,
            "ftp": proxies,
        }
        self.chunk = chunk
        self.timeout = timeout

    def __init_root(self, root: Path, path: str, folder: str) -> Path:
        if path and (r := Path(path)).is_dir():
            root = r.joinpath(folder or "Download")
        else:
            root = root.joinpath(folder or "Download")
        root.mkdir(exist_ok=True)
        self.temp.mkdir(exist_ok=True)
        return root

    def run(self, urls: list, name: str, type_: int):
        if type_ == 0:
            self.__download(urls[0], f"{name}.mp4")
        elif type_ == 1:
            for index, url in enumerate(urls):
                self.__download(url, f"{name}_{index + 1}.png")

    def __download(self, url: str, name: str):
        temp = self.temp.joinpath(name)
        file = self.root.joinpath(name)
        if self.manager.is_exists(file):
            return
        try:
            with get(url, headers=self.headers, proxies=self.proxies, stream=True, timeout=self.timeout) as response:
                with temp.open("wb") as f:
                    for chunk in response.iter_content(chunk_size=self.chunk):
                        f.write(chunk)
            self.manager.move(temp, file)
        except (
                exceptions.ProxyError,
                exceptions.SSLError,
                exceptions.ChunkedEncodingError,
                exceptions.ConnectionError,
                exceptions.ReadTimeout,
        ):
            self.manager.delete(temp)

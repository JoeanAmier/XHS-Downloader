from pathlib import Path

from aiohttp import ClientConnectionError
from aiohttp import ClientProxyConnectionError
from aiohttp import ClientSSLError
from aiohttp import ClientSession

# from aiohttp import ClientTimeout

__all__ = ['Download']


class Download:

    def __init__(
            self,
            manager,
            root: Path,
            path: str,
            folder: str,
            proxy: str = None,
            chunk=1024 * 1024,
            timeout=10, ):
        self.manager = manager
        self.temp = manager.temp
        self.root = self.__init_root(root, path, folder)
        self.proxy = proxy
        self.chunk = chunk
        # self.timeout = ClientTimeout(total=timeout)
        self.session = ClientSession(headers=manager.headers)

    def __init_root(self, root: Path, path: str, folder: str) -> Path:
        if path and (r := Path(path)).is_dir():
            root = r.joinpath(folder or "Download")
        else:
            root = root.joinpath(folder or "Download")
        root.mkdir(exist_ok=True)
        self.temp.mkdir(exist_ok=True)
        return root

    async def run(self, urls: list, name: str, type_: int, log, bar):
        if type_ == 0:
            await self.__download(urls[0], f"{name}.mp4", log, bar)
        elif type_ == 1:
            for index, url in enumerate(urls):
                await self.__download(url, f"{name}_{index + 1}.png", log, bar)

    async def __download(self, url: str, name: str, log, bar):
        temp = self.temp.joinpath(name)
        file = self.root.joinpath(name)
        if self.manager.is_exists(file):
            return
        try:
            async with self.session.get(url, proxy=self.proxy) as response:
                # self.__create_progress(bar, int(response.headers.get('content-length', 0)))
                with temp.open("wb") as f:
                    async for chunk in response.content.iter_chunked(self.chunk):
                        f.write(chunk)
                        # self.__update_progress(bar, len(chunk))
                # self.__remove_progress(bar)
            self.manager.move(temp, file)
        except (
                ClientProxyConnectionError,
                ClientSSLError,
                ClientConnectionError,
                TimeoutError,
        ):
            self.manager.delete(temp)
            # self.__remove_progress(bar)

    # @staticmethod
    # def __create_progress(bar, total: int | None):
    #     if bar:
    #         bar.update(total=total)
    #
    # @staticmethod
    # def __update_progress(bar, advance: int):
    #     if bar:
    #         bar.advance(advance)
    #
    # @staticmethod
    # def __remove_progress(bar):
    #     pass

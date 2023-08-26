from pathlib import Path


class Download:
    def __init__(
            self,
            path,
            headers: dict,
            proxies=None, ):
        self.root = Path(path)
        self.headers = headers
        self.proxies = {
            "http": proxies,
            "https": proxies,
            "ftp": proxies,
        }

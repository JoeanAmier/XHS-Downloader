class Download:
    def __init__(
            self,
            headers: dict,
            proxies=None, ):
        self.headers = headers
        self.proxies = {
            "http": proxies,
            "https": proxies,
            "ftp": proxies,
        }

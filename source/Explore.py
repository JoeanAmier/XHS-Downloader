from re import compile


class Explore:
    explore_data = compile(r'"noteDetailMap": (\{.*?})')

    def __init__(self, html, url: str):
        self.html = html
        self.url = url

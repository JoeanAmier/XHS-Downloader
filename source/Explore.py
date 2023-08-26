from re import compile


class Explore:
    explore_data = compile(r'"noteDetailMap": (\{.*?})')

    def __init__(self, html: str):
        self.html = html

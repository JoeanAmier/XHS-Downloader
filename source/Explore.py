from json import loads
from re import compile


class Explore:
    explore_data = compile(
        r'"currentTime":\d{13},"note":(.*?)}},"serverRequestInfo"')

    def run(self, html: str):
        data = self.get_json_data(html)

    def get_json_data(self, html: str) -> dict:
        data = self.explore_data.findall(html)
        return {} if len(data) != 1 else loads(data[0])

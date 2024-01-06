from lxml.etree import HTML
from yaml import safe_load

__all__ = ["Converter"]


class Converter:
    INITIAL_STATE = "(//script)[last()]/text()"
    KEYS_LINK = (
        "note",
        "noteDetailMap",
        "[-1]",
        "note",
    )

    def run(self, content: str) -> dict:
        return self.__filter_object(
            self.__convert_object(
                self.__extract_object(content)))

    def __extract_object(self, html: str) -> str:
        html_tree = HTML(html)
        return d[0] if (d := html_tree.xpath(self.INITIAL_STATE)) else ""

    @staticmethod
    def __convert_object(text: str) -> dict:
        return safe_load(text.lstrip("window.__INITIAL_STATE__="))

    @classmethod
    def __filter_object(cls, data: dict) -> dict:
        return cls.deep_get(data, cls.KEYS_LINK) or {}

    @classmethod
    def deep_get(cls, data: dict, keys: list | tuple, default=None):
        try:
            for key in keys:
                if key.startswith("[") and key.endswith("]"):
                    data = cls.safe_get(data, int(key[1:-1]))
                else:
                    data = data[key]
            return data
        except (KeyError, IndexError, ValueError):
            return default

    @staticmethod
    def safe_get(data: dict | list | tuple | set, index: int):
        if isinstance(data, dict):
            return list(data.values())[index]
        elif isinstance(data, list | tuple | set):
            return data[index]
        raise TypeError

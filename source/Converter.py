from copy import deepcopy
from types import SimpleNamespace

from lxml.etree import HTML
from yaml import safe_load

__all__ = ["Converter", "Namespace"]


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


class Namespace:
    def __init__(self, data: dict):
        self.data = self.generate_data_object(data)

    @staticmethod
    def generate_data_object(data: dict) -> SimpleNamespace:
        def depth_conversion(element):
            if isinstance(element, dict):
                return SimpleNamespace(
                    **{k: depth_conversion(v) for k, v in element.items()})
            elif isinstance(element, list):
                return [depth_conversion(item) for item in element]
            else:
                return element

        return depth_conversion(data)

    def safe_extract(
            self,
            attribute_chain: str,
            default: str | int | list | dict | SimpleNamespace = ""):
        return self.__safe_extract(self.data, attribute_chain, default)

    @staticmethod
    def __safe_extract(
            data_object,
            attribute_chain: str,
            default: str | int | list | dict | SimpleNamespace = "", ):
        data = deepcopy(data_object)
        attributes = attribute_chain.split(".")
        for attribute in attributes:
            if "[" in attribute:
                parts = attribute.split("[", 1)
                attribute = parts[0]
                index = parts[1].split("]", 1)[0]
                try:
                    index = int(index)
                    data = getattr(data, attribute, None)[index]
                except (IndexError, TypeError, ValueError):
                    return default
            else:
                data = getattr(data, attribute, None)
                if not data:
                    return default
        return data or default

    @classmethod
    def object_extract(
            cls,
            data_object: SimpleNamespace,
            attribute_chain: str,
            default: str | int | list | dict | SimpleNamespace = "",
    ):
        return cls.__safe_extract(
            data_object,
            attribute_chain,
            default, )

    def __dict__(self):
        return vars(self.data)

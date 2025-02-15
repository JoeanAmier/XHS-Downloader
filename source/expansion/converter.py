from typing import Union

from lxml.etree import HTML
from yaml import safe_load

__all__ = ["Converter"]


class Converter:
    INITIAL_STATE = "//script/text()"
    KEYS_LINK = (
        "note",
        "noteDetailMap",
        "[-1]",
        "note",
    )

    def run(self, content: str) -> dict:
        return self._filter_object(self._convert_object(self._extract_object(content)))

    def _extract_object(self, html: str) -> str:
        if not html:
            return ""
        html_tree = HTML(html)
        scripts = html_tree.xpath(self.INITIAL_STATE)
        return self.get_script(scripts)

    @staticmethod
    def _convert_object(text: str) -> dict:
        return safe_load(text.lstrip("window.__INITIAL_STATE__="))

    @classmethod
    def _filter_object(cls, data: dict) -> dict:
        return cls.deep_get(data, cls.KEYS_LINK) or {}

    @classmethod
    def deep_get(cls, data: dict, keys: list | tuple, default=None):
        if not data:
            return default
        try:
            for key in keys:
                if key.startswith("[") and key.endswith("]"):
                    data = cls.safe_get(data, int(key[1:-1]))
                else:
                    data = data[key]
            return data
        except (KeyError, IndexError, ValueError, TypeError):
            return default

    @staticmethod
    def safe_get(data: Union[dict, list, tuple, set], index: int):
        if isinstance(data, dict):
            return list(data.values())[index]
        elif isinstance(data, list | tuple | set):
            return data[index]
        raise TypeError

    @staticmethod
    def get_script(scripts: list) -> str:
        scripts.reverse()
        for script in scripts:
            if script.startswith("window.__INITIAL_STATE__"):
                return script
        return ""

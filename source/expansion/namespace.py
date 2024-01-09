from copy import deepcopy
from types import SimpleNamespace
from typing import Union

__all__ = ["Namespace"]


class Namespace:
    def __init__(self, data: dict) -> None:
        self.data: SimpleNamespace = self.generate_data_object(data)

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
            default: Union[str, int, list, dict, SimpleNamespace] = ""):
        return self.__safe_extract(self.data, attribute_chain, default)

    @staticmethod
    def __safe_extract(
            data_object: SimpleNamespace,
            attribute_chain: str,
            default: Union[str, int, list, dict, SimpleNamespace] = "", ):
        data = deepcopy(data_object)
        attributes = attribute_chain.split(".")
        for attribute in attributes:
            if "[" in attribute:
                parts = attribute.split("[", 1)
                attribute = parts[0]
                index = parts[1][:-1]
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
            default: Union[str, int, list, dict, SimpleNamespace] = "",
    ):
        return cls.__safe_extract(
            data_object,
            attribute_chain,
            default, )

    @property
    def __dict__(self):
        return self.convert_to_dict(self.data)

    @classmethod
    def convert_to_dict(cls, data) -> dict:
        return {
            key: cls.convert_to_dict(value) if isinstance(
                value,
                SimpleNamespace) else value for key,
            value in vars(data).items()}

    def __bool__(self):
        return bool(vars(self.data))

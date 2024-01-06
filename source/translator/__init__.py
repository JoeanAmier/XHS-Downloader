from .chinese import Chinese
from .english import English

__all__ = [
    "LANGUAGE",
    "Chinese",
    "English",
]

LANGUAGE = {
    Chinese.code: Chinese,
    English.code: English,
}

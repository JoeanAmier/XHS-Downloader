from gettext import translation

from ..module import ROOT

__all__ = ["Translate"]


class Translate:
    SUPPORT = {
        "zh_CN",
        "en_GB",
    }

    def __init__(self, language: str):
        self.language = self.__check_language(language)
        self.translate = translation(
            "xhs",
            localedir=ROOT.joinpath("locale"),
            languages=[self.language],
            fallback=True,
        )

    def __check_language(self, language: str) -> str:
        return language if language in self.SUPPORT else "zh_CN"

    def message(self):
        return self.translate.gettext

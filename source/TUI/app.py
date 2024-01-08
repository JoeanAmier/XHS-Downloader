from textual.app import App

from source.application import XHS
from source.module import (
    ROOT,
)
from source.module import Settings
from source.translator import Chinese
from source.translator import LANGUAGE
from .index import Index
from .setting import Setting

__all__ = ["XHSDownloader"]


class XHSDownloader(App):
    def __init__(self):
        super().__init__()
        self.settings = Settings(ROOT)
        self.parameter = self.settings.run()
        self.prompt = LANGUAGE.get(self.parameter["language"], Chinese)
        self.APP = XHS(**self.parameter, language_object=self.prompt)

    async def __aenter__(self):
        await self.APP.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.APP.__aexit__(exc_type, exc_value, traceback)

    async def on_mount(self) -> None:
        self.install_screen(Setting(), name="setting")
        self.install_screen(Index(self.APP, self.prompt), name="index")
        await self.push_screen("index")

    async def action_settings(self):
        await self.push_screen("setting")

    async def action_back(self):
        await self.push_screen("index")

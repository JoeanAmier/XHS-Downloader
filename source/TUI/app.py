from typing import Type

from textual.app import App
from textual.widgets import RichLog

from source.application import XHS
from source.module import (
    ROOT,
)
from source.module import Settings
from source.translator import (
    LANGUAGE,
    Chinese,
    English,
)
# from .about import About
from .index import Index
from .loading import Loading
from .monitor import Monitor
from .record import Record
from .setting import Setting
from .update import Update

__all__ = ["XHSDownloader"]


class XHSDownloader(App):
    CSS_PATH = ROOT.joinpath("static/XHS-Downloader.tcss")
    SETTINGS = Settings(ROOT)

    def __init__(self):
        super().__init__()
        self.parameter: dict
        self.prompt: Type[Chinese | English]
        self.APP: XHS
        self.__initialization()

    async def __aenter__(self):
        await self.APP.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.APP.__aexit__(exc_type, exc_value, traceback)

    def __initialization(self) -> None:
        self.parameter = self.SETTINGS.run()
        self.prompt = LANGUAGE.get(self.parameter["language"], Chinese)
        self.APP = XHS(**self.parameter, language_object=self.prompt)

    async def on_mount(self) -> None:
        self.install_screen(
            Setting(
                self.parameter,
                self.prompt),
            name="setting")
        self.install_screen(Index(self.APP, self.prompt), name="index")
        self.install_screen(Loading(self.prompt), name="loading")
        # self.install_screen(About(self.prompt), name="about")
        self.install_screen(Record(self.APP, self.prompt), name="record")
        await self.push_screen("index")

    async def action_settings(self):
        async def save_settings(data: dict) -> None:
            self.SETTINGS.update(data)
            await self.refresh_screen()

        await self.push_screen("setting", save_settings)

    async def action_about(self):
        await self.push_screen("about")

    async def action_index(self):
        await self.push_screen("index")

    async def action_record(self):
        await self.push_screen("record")

    async def refresh_screen(self):
        self.pop_screen()
        await self.APP.recorder.database.close()
        await self.APP.close()
        self.__initialization()
        await self.__aenter__()
        self.uninstall_screen("index")
        self.uninstall_screen("setting")
        self.uninstall_screen("loading")
        # self.uninstall_screen("about")
        self.uninstall_screen("record")
        self.install_screen(Index(self.APP, self.prompt), name="index")
        self.install_screen(
            Setting(
                self.parameter,
                self.prompt),
            name="setting")
        self.install_screen(Loading(self.prompt), name="loading")
        # self.install_screen(About(self.prompt), name="about")
        self.install_screen(Record(self.APP, self.prompt), name="record")
        await self.push_screen("index")

    def update_result(self, tip: str) -> None:
        log = self.query_one(RichLog)
        log.write(tip)
        log.write(">" * 50)

    async def action_check_update(self):
        await self.push_screen(Update(self.APP, self.prompt), callback=self.update_result)

    async def action_check_update_about(self):
        await self.push_screen("index")
        await self.action_check_update()

    async def action_monitor(self):
        await self.push_screen(Monitor(self.APP, self.prompt))

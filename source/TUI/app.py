from textual.app import App
from textual.widgets import RichLog

from ..application import XHS
from ..module import (
    ERROR,
    ROOT,
    Settings,
    logging,
)
from ..translation import _
from .about import About
from .index import Index
from .loading import Loading
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
        self.APP: XHS
        self.__initialization()

    async def __aenter__(self):
        await self.APP.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.APP.__aexit__(exc_type, exc_value, traceback)

    def __initialization(self) -> None:
        self.parameter = self.SETTINGS.run()
        self.APP = XHS(
            **self.parameter,
            _print=False,
        )

    async def on_mount(self) -> None:
        self.theme = "nord"
        self.install_screen(
            Setting(
                self.parameter,
            ),
            name="setting",
        )
        self.install_screen(
            Index(
                self.APP,
            ),
            name="index",
        )
        self.install_screen(Loading(), name="loading")
        self.install_screen(About(), name="about")
        self.install_screen(
            Record(
                self.APP,
            ),
            name="record",
        )
        await self.push_screen("index")
        self.SETTINGS.check_keys(
            self.parameter,
            logging,
            self.screen.query_one(RichLog),
            _(
                "配置文件 settings.json 缺少必要的参数，请删除该文件，然后重新运行程序，自动生成默认配置文件！"
            )
            + f"\n{'>' * 50}",
            ERROR,
        )

    async def action_settings(self):
        async def save_settings(data: dict) -> None:
            self.SETTINGS.update(data)
            await self.refresh_screen()

        await self.push_screen("setting", save_settings)

    async def refresh_screen(self):
        await self.action_back()
        await self.close_database()
        await self.APP.close()
        self.__initialization()
        await self.__aenter__()
        self.uninstall_screen("index")
        self.uninstall_screen("setting")
        self.uninstall_screen("loading")
        self.uninstall_screen("about")
        self.uninstall_screen("record")
        self.install_screen(
            Index(
                self.APP,
            ),
            name="index",
        )
        self.install_screen(
            Setting(
                self.parameter,
            ),
            name="setting",
        )
        self.install_screen(Loading(), name="loading")
        self.install_screen(About(), name="about")
        self.install_screen(
            Record(
                self.APP,
            ),
            name="record",
        )
        await self.push_screen("index")

    def update_result(self, args: tuple[str, str]) -> None:
        self.notify(
            args[0],
            severity=args[1],
        )

    async def action_update(self):
        await self.push_screen(
            Update(
                self.APP,
            ),
            callback=self.update_result,
        )

    async def close_database(self):
        await self.APP.id_recorder.cursor.close()
        await self.APP.id_recorder.database.close()
        await self.APP.data_recorder.cursor.close()
        await self.APP.data_recorder.database.close()

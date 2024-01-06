from webbrowser import open

from pyperclip import paste
from rich.text import Text
from textual.app import App
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center
from textual.containers import HorizontalScroll
from textual.containers import ScrollableContainer
from textual.widgets import Button
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import ProgressBar
from textual.widgets import RichLog

from source.application import XHS
from source.module import Settings
from source.module import (
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_BETA,
    ROOT,
    PROMPT,
    MASTER,
    ERROR,
    WARNING,
    INFO,
    LICENCE,
    REPOSITORY,
    RELEASES,
    GENERAL,
    USERSCRIPT,
)
from source.translator import Chinese
from source.translator import LANGUAGE
from .setting import Setting

__all__ = ["XHSDownloader"]


def show_state(function):
    async def inner(self, *args, **kwargs):
        self.close_disclaimer()
        self.bar.update(total=100, progress=100)
        result = await function(self, *args, **kwargs)
        self.bar.update(total=None)
        self.tip.write(Text(">" * 50, style=GENERAL))
        return result

    return inner


class XHSDownloader(App):
    CSS_PATH = ROOT.joinpath(
        "static/css/index.tcss")
    BINDINGS = [
        Binding(key="q", action="quit", description="退出程序"),
        # ("d", "toggle_dark", "切换主题"),
        Binding(key="u", action="check_update", description="检查更新"),
        Binding(key="m", action="user_script", description="获取脚本"),
        # Binding(key="l", action="choose_language", description="切换语言"),
        # Binding(key="s", action="settings", description="程序设置"),
    ]

    def __init__(self):
        super().__init__()
        settings = Settings(ROOT).run()
        self.prompt = LANGUAGE.get(settings["language"], Chinese)
        self.APP = XHS(**settings, language_object=self.prompt)
        self.url = None
        self.tip = None
        self.bar = None
        self.setting = None
        self.disclaimer = True

    async def __aenter__(self):
        await self.APP.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.APP.__aexit__(exc_type, exc_value, traceback)

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(Label(Text(f"{self.prompt.open_source_protocol}{LICENCE}", style=MASTER)),
                                  Label(
                                      Text(
                                          f"{self.prompt.project_address}{REPOSITORY}",
                                          style=MASTER)),
                                  Label(Text(self.prompt.input_box_title,
                                             style=PROMPT), id="prompt"),
                                  Input(placeholder=self.prompt.input_prompt),
                                  HorizontalScroll(Button(self.prompt.download_button, id="deal"),
                                                   Button(self.prompt.paste_button, id="paste"),
                                                   Button(self.prompt.reset_button, id="reset"), ),
                                  id="index",
                                  )
        with Center():
            yield ProgressBar(total=None, show_percentage=False, show_eta=False)
        yield RichLog(markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"XHS-Downloader V{VERSION_MAJOR}.{
        VERSION_MINOR}{" Beta" if VERSION_BETA else ""}"

    def on_ready(self) -> None:
        self.url = self.query_one(Input)
        self.tip = self.query_one(RichLog)
        self.bar = self.query_one(ProgressBar)
        self.tip.write(Text("\n".join(self.prompt.disclaimer), style=MASTER))

    def close_disclaimer(self):
        if self.disclaimer:
            self.tip.clear()
            self.disclaimer = False

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "deal":
            await self.deal()
        elif event.button.id == "reset":
            self.query_one(Input).value = ""
        elif event.button.id == "paste":
            self.query_one(Input).value = paste()

    @show_state
    async def deal(self):
        if not self.url.value:
            self.tip.write(Text(self.prompt.invalid_link, style=WARNING))
            return
        if any(await self.APP.extract(self.url.value, True, log=self.tip)):
            self.url.value = ""
        else:
            self.tip.write(Text(self.prompt.download_failure, style=ERROR))

    @show_state
    async def action_check_update(self):
        self.tip.write(
            Text(
                self.prompt.check_update_notification,
                style=WARNING))
        try:
            url = await self.APP.html.request_url(RELEASES, False, self.tip)
            latest_major, latest_minor = map(
                int, url.split("/")[-1].split(".", 1))
            if latest_major > VERSION_MAJOR or latest_minor > VERSION_MINOR:
                self.tip.write(
                    Text(
                        self.prompt.official_version_update(
                            latest_major,
                            latest_minor),
                        style=WARNING))
                self.tip.write(RELEASES)
            elif latest_minor == VERSION_MINOR and VERSION_BETA:
                self.tip.write(
                    Text(
                        self.prompt.development_version_update,
                        style=WARNING))
                self.tip.write(RELEASES)
            elif VERSION_BETA:
                self.tip.write(
                    Text(
                        self.prompt.latest_development_version,
                        style=WARNING))
            else:
                self.tip.write(
                    Text(
                        self.prompt.latest_official_version,
                        style=INFO))
        except ValueError:
            self.tip.write(Text(self.prompt.check_update_failure, style=ERROR))

    @staticmethod
    def action_user_script():
        open(USERSCRIPT)

    def action_choose_language(self):
        pass

    def action_settings(self):
        if self.setting:
            self.setting.remove()
            self.setting = None
        else:
            self.setting = Setting()
            self.query_one("#index").mount(self.setting)

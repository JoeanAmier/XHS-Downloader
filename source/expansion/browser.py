from contextlib import suppress
from sys import platform

from rich.console import Console
from rookiepy import (
    arc,
    brave,
    chrome,
    chromium,
    edge,
    firefox,
    librewolf,
    opera,
    opera_gx,
    vivaldi,
)

try:
    from source.translation import _
except ImportError:
    _ = lambda s: s

__all__ = ["BrowserCookie"]


class BrowserCookie:
    SUPPORT_BROWSER = {
        "Arc": (arc, "Linux, macOS, Windows"),
        "Chrome": (chrome, "Linux, macOS, Windows"),
        "Chromium": (chromium, "Linux, macOS, Windows"),
        "Opera": (opera, "Linux, macOS, Windows"),
        "OperaGX": (opera_gx, "macOS, Windows"),
        "Brave": (brave, "Linux, macOS, Windows"),
        "Edge": (edge, "Linux, macOS, Windows"),
        "Vivaldi": (vivaldi, "Linux, macOS, Windows"),
        "Firefox": (firefox, "Linux, macOS, Windows"),
        "LibreWolf": (librewolf, "Linux, macOS, Windows"),
    }

    @classmethod
    def run(
        cls,
        domains: list[str],
        console: Console = None,
    ) -> str:
        console = console or Console()
        options = "\n".join(
            f"{i}. {k}: {v[1]}"
            for i, (k, v) in enumerate(cls.SUPPORT_BROWSER.items(), start=1)
        )
        if browser := console.input(
            _(
                "读取指定浏览器的 Cookie 并写入配置文件\n"
                "Windows 系统需要以管理员身份运行程序才能读取 Chromium、Chrome、Edge 浏览器 Cookie！\n"
                "{options}\n请输入浏览器名称或序号："
            ).format(options=options),
        ):
            return cls.get(
                browser,
                domains,
                console,
            )
        console.print(_("未选择浏览器！"))

    @classmethod
    def get(
        cls,
        browser: str | int,
        domains: list[str],
        console: Console = None,
    ) -> str:
        console = console or Console()
        if not (browser := cls.__browser_object(browser)):
            console.print(_("浏览器名称或序号输入错误！"))
            return ""
        try:
            cookies = browser(domains=domains)
            return "; ".join(f"{i['name']}={i['value']}" for i in cookies)
        except RuntimeError:
            console.print(_("获取 Cookie 失败，未找到 Cookie 数据！"))
        return ""

    @classmethod
    def __browser_object(cls, browser: str | int):
        with suppress(ValueError):
            browser = int(browser) - 1
        if isinstance(browser, int):
            try:
                return list(cls.SUPPORT_BROWSER.values())[browser][0]
            except IndexError:
                return None
        if isinstance(browser, str):
            try:
                return cls.__match_browser(browser)
            except KeyError:
                return None
        raise TypeError

    @classmethod
    def __match_browser(cls, browser: str):
        for i, j in cls.SUPPORT_BROWSER.items():
            if i.lower() == browser.lower():
                return j[0]


match platform:
    case "darwin":
        from rookiepy import safari

        BrowserCookie.SUPPORT_BROWSER |= {
            "Safari": (safari, "macOS"),
        }
    case "linux":
        BrowserCookie.SUPPORT_BROWSER.pop("OperaGX")
    case "win32":
        pass
    case _:
        print(_("从浏览器读取 Cookie 功能不支持当前平台！"))

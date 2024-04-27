from browser_cookie3 import (
    chrome,
    chromium,
    opera,
    opera_gx,
    brave,
    edge,
    vivaldi,
    firefox,
    librewolf,
    safari,
    BrowserCookieError,
)

__all__ = ["BrowserCookie"]


class BrowserCookie:
    SUPPORT_BROWSER = {
        "chrome": chrome,
        "chromium": chromium,
        "opera": opera,
        "opera_gx": opera_gx,
        "brave": brave,
        "edge": edge,
        "vivaldi": vivaldi,
        "firefox": firefox,
        "librewolf": librewolf,
        "safari": safari,
    }

    @classmethod
    def get(cls, browser: str | int, domain: str) -> str:
        browser = cls.__browser_object(browser)
        try:
            cookie = browser(domain_name=domain)
            cookie = [f"{i.name}={i.value}" for i in cookie]
            return "; ".join(cookie)
        except PermissionError:
            print("读取 Cookie 失败，浏览器未关闭！")
        except BrowserCookieError:
            print("获取 Cookie 失败，未找到 Cookie 数据！")
        return ""

    @classmethod
    def __browser_object(cls, browser: str | int):
        if isinstance(browser, str):
            return cls.SUPPORT_BROWSER[browser.lower()]
        elif isinstance(browser, int):
            return list(cls.SUPPORT_BROWSER.values())[browser - 1]
        raise TypeError

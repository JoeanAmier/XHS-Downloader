"""Read login cookies from a dedicated Xiaohongshu WebView window."""

from contextlib import suppress
from datetime import datetime
from http.cookies import SimpleCookie
from json import dumps
from pathlib import Path
from threading import Event, Lock, Thread
from time import monotonic
from typing import Any, Callable
from urllib.parse import parse_qs, urlsplit

import webview

from ..module import ROOT, VOLUME
from ..translation import _

LOGIN_URL = "https://www.xiaohongshu.com/explore"
LOGIN_SCRIPT_PATH = ROOT / "static/GUI/qr_login.js"


def is_login_origin(url: str) -> bool:
    parts = urlsplit(url)
    return parts.scheme == "https" and parts.hostname == "www.xiaohongshu.com"


def collect_login_cookies(jars: list[SimpleCookie]) -> dict[str, Any]:
    """Keep only Xiaohongshu cookies, including cookies marked HttpOnly."""

    values = {}
    for jar in jars:
        for name, cookie in jar.items():
            domain = cookie["domain"].lower().lstrip(".")
            if domain and not (
                domain == "xiaohongshu.com" or domain.endswith(".xiaohongshu.com")
            ):
                continue
            values[name] = cookie
    return values


class QrLogin:
    """Own the login window and a bounded polling thread; never log cookies."""

    def __init__(
        self,
        timeout: float = 300,
        poll_interval: float = 1,
        on_success: Callable[[str], None] | None = None,
        diagnostic_path: Path | None = VOLUME / "qr-login.log",
    ):
        self._timeout = timeout
        self._poll_interval = poll_interval
        self._lock = Lock()
        self._window = None
        self._stop = Event()
        self._result: dict[str, Any] = {"status": "idle"}
        self._on_success = on_success
        self._diagnostic_path = diagnostic_path
        self._diagnostic_lock = Lock()

    def _diagnose(self, event: str, **fields) -> None:
        # Only callers' fixed flags/counts are logged, never page contents,
        # cookie values, account identifiers or exception messages.
        if self._diagnostic_path is None:
            return
        with self._diagnostic_lock, suppress(OSError):
            with self._diagnostic_path.open("a", encoding="utf-8") as log:
                log.write(dumps({"time": datetime.now().isoformat(timespec="seconds"),
                                 "event": event, **fields}, ensure_ascii=False) + "\n")

    def start(self) -> dict[str, Any]:
        with self._lock:
            if self._window is not None:
                self._window.show()
                return dict(self._result)
            # No js_api is exposed to the external website.
            window = webview.create_window(
                _("小红书扫码登录"),
                LOGIN_URL,
                width=560,
                height=680,
                min_size=(480, 560),
                text_select=True,
            )
            stop = Event()
            self._window = window
            self._stop = stop
            self._result = {"status": "waiting"}
            self._diagnose("started")

            def on_closed():
                stop.set()
                with self._lock:
                    if self._window is window:
                        self._window = None
                        if self._result["status"] == "waiting":
                            self._result = {"status": "cancelled"}
                self._diagnose("window_closed")

            window.events.closed += on_closed
            Thread(
                target=self._poll,
                args=(window, stop),
                name="xhs-qr-login",
                daemon=True,
            ).start()
            return dict(self._result)

    def state(self) -> dict[str, Any]:
        with self._lock:
            return {**self._result, "can_capture": self._window is not None}

    def confirm_import(self) -> None:
        self._diagnose("cookie_filled_in_settings")

    def capture(self) -> dict[str, Any]:
        """Export the current window's cookies on an explicit user request.

        This action does not depend on site DOM or claim that an anonymous
        session is authenticated. The user can use it after reaching home.
        """
        with self._lock:
            window = self._window
            result = dict(self._result)
        if result["status"] == "success":
            return self.state()
        if window is None:
            return {"status": "error", "message": _("请先打开扫码登录窗口")}
        try:
            if not is_login_origin(window.get_current_url() or ""):
                return {"status": "error", "message": _("请在小红书登录页面读取 Cookie")}
            cookies = collect_login_cookies(window.get_cookies() or [])
            self._diagnose("manual_read", cookie_count=len(cookies),
                           has_session=bool(cookies.get("web_session")))
            if not cookies.get("web_session") or not cookies["web_session"].value:
                return {"status": "error", "message": _("尚未读取到会话 Cookie，请完成登录后再试")}
            self._finish(window, {"status": "success", "cookie": self._cookie_header(cookies)})
            return self.state()
        except Exception as error:
            self._diagnose("manual_read_failed", error_type=type(error).__name__)
            return {"status": "error", "message": _("读取 Cookie 失败，请保持登录窗口打开后重试")}

    @staticmethod
    def _cookie_header(cookies) -> str:
        return "; ".join(f"{name}={cookie.coded_value}" for name, cookie in cookies.items())

    def close(self) -> None:
        with self._lock:
            window = self._window
            self._window = None
            self._stop.set()
            self._result = {"status": "cancelled"}
        if window is not None:
            with suppress(Exception):
                window.destroy()

    def _finish(self, window, result: dict[str, Any]) -> None:
        with self._lock:
            if self._window is not window or self._stop.is_set():
                return
            self._result = result
        self._diagnose("completed", status=result["status"])
        if result["status"] == "success" and self._on_success:
            try:
                self._on_success(result["cookie"])
                self._diagnose("settings_notified")
            except Exception as error:
                self._diagnose("settings_notification_failed", error_type=type(error).__name__)
        # Destroy outside the lock: closed handlers may run synchronously.
        with suppress(Exception):
            window.destroy()

    def _poll(self, window, stop: Event) -> None:
        deadline = monotonic() + self._timeout
        initial_qr_session = None
        saw_qr = False
        last_diagnostic = None
        try:
            script = LOGIN_SCRIPT_PATH.read_text(encoding="utf-8")
            while not stop.wait(self._poll_interval):
                if monotonic() >= deadline:
                    # Keep a successfully signed-in browser available for the
                    # manual export instead of discarding its private session.
                    with self._lock:
                        if self._window is window and self._result["status"] == "waiting":
                            self._result = {"status": "error", "message": _("未能自动确认登录；若已进入首页，请点击“读取 Cookie”")}
                    self._diagnose("auto_detection_timeout")
                    return
                if not window.events.loaded.is_set():
                    continue
                try:
                    url = window.get_current_url() or ""
                    if not is_login_origin(url):
                        continue
                    parts = urlsplit(url)
                    if parts.path.startswith("/website-login/error"):
                        message = parse_qs(parts.query).get("error_msg", [""])[0]
                        self._finish(window, {
                            "status": "error",
                            "message": message or _("小红书登录页面加载失败，请重试"),
                        })
                        return
                    # Read native cookies first. Page JS failing after a login
                    # navigation must not prevent access to the cookie store.
                    cookies = collect_login_cookies(window.get_cookies() or [])
                except Exception as error:
                    # Navigation after scanning can briefly replace the JS context.
                    self._diagnose("native_read_failed", error_type=type(error).__name__)
                    continue
                page = {}
                try:
                    value = window.evaluate_js(script)
                    if isinstance(value, dict):
                        page = value
                except Exception as error:
                    self._diagnose("page_detection_failed", error_type=type(error).__name__)
                session = cookies.get("web_session")
                session_value = session.value if session else ""
                diagnostic = (len(cookies), bool(session_value), page.get("login_visible"),
                              page.get("qr_visible"), page.get("authenticated"), page.get("state_shape"))
                if diagnostic != last_diagnostic:
                    self._diagnose("observed", cookie_count=diagnostic[0], has_session=diagnostic[1],
                                   login_visible=diagnostic[2], qr_visible=diagnostic[3],
                                   authenticated=diagnostic[4], state_shape=diagnostic[5])
                    last_diagnostic = diagnostic
                authenticated = page.get("authenticated", False)
                if session_value and (
                    authenticated
                    or (
                        saw_qr
                        and page.get("login_visible") is False
                        and session_value != initial_qr_session
                    )
                ):
                    self._finish(window, {"status": "success", "cookie": self._cookie_header(cookies)})
                    return
                if page.get("qr_visible") and not saw_qr:
                    # Preserve the pre-scan value. The cookie can change before
                    # the QR modal closes, so updating it on every poll loses
                    # the evidence that a new session was established.
                    initial_qr_session = session_value
                    saw_qr = True
        except Exception:
            if not stop.is_set():
                self._finish(window, {
                    "status": "error",
                    "message": _("读取登录状态失败，请关闭登录窗口后重试"),
                })

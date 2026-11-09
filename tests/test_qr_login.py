import threading
import time
import unittest
from http.cookies import SimpleCookie
from types import SimpleNamespace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from source.GUI.login import QrLogin, collect_login_cookies, is_login_origin


def jar(value, domain=".xiaohongshu.com", httponly=False):
    result = SimpleCookie()
    result.load(value)
    for item in result.values():
        item["domain"] = domain
        item["httponly"] = httponly
    return result


class ClosedEvent:
    def __init__(self):
        self.callbacks = []

    def __iadd__(self, callback):
        self.callbacks.append(callback)
        return self

    def fire(self):
        for callback in self.callbacks:
            callback()


class LoginWindow:
    def __init__(self):
        loaded = threading.Event()
        loaded.set()
        self.events = SimpleNamespace(loaded=loaded, closed=ClosedEvent())
        self.page = {"login_visible": True, "qr_visible": True, "authenticated": False}
        self.cookies = [jar("a1=anonymous; web_session=anonymous")]
        self.url = "https://www.xiaohongshu.com/explore"
        self.closed = False
        self.shown = 0
        self.cookie_reads = 0

    def get_current_url(self):
        return self.url

    def evaluate_js(self, script):
        return self.page

    def get_cookies(self):
        self.cookie_reads += 1
        return self.cookies

    def destroy(self):
        self.closed = True
        self.events.closed.fire()

    def show(self):
        self.shown += 1


class QrLoginTests(unittest.TestCase):
    def setUp(self):
        self.window = LoginWindow()
        self.controller = QrLogin(timeout=2, poll_interval=0.01, diagnostic_path=None)
        self.create = patch("source.GUI.login.webview.create_window", return_value=self.window)
        self.factory = self.create.start()

    def tearDown(self):
        self.controller.close()
        self.create.stop()

    def until(self, predicate):
        deadline = time.monotonic() + 2
        while not predicate():
            if time.monotonic() >= deadline:
                self.fail("Login state did not change before timeout")
            time.sleep(0.01)

    def test_imports_httponly_cookie_after_authenticated_login(self):
        self.controller.start()
        self.until(lambda: self.window.cookie_reads > 0)
        self.assertEqual(self.controller.state()["status"], "waiting")
        self.window.cookies = [jar("a1=visitor"), jar("web_session=logged-in", httponly=True), jar("secret=foreign", "example.com")]
        self.window.page = {"authenticated": True, "login_visible": False, "qr_visible": False}
        self.until(lambda: self.controller.state()["status"] == "success")
        self.until(lambda: self.window.closed)
        cookie = self.controller.state()["cookie"]
        self.assertIn("a1=visitor", cookie)
        self.assertIn("web_session=logged-in", cookie)
        self.assertNotIn("HttpOnly", cookie)
        self.assertNotIn("foreign", cookie)
        self.assertNotIn("js_api", self.factory.call_args.kwargs)

    def test_closing_login_modal_does_not_import_anonymous_session(self):
        self.controller.start()
        self.until(lambda: self.window.cookie_reads > 0)
        self.window.page = {"authenticated": False, "login_visible": False, "qr_visible": False}
        time.sleep(0.05)
        self.assertEqual(self.controller.state()["status"], "waiting")
        self.assertNotIn("cookie", self.controller.state())

    def test_detects_changed_session_after_qr_modal_disappears(self):
        self.controller.start()
        self.until(lambda: self.window.cookie_reads > 0)
        self.window.page = {"authenticated": False, "login_visible": False, "qr_visible": False}
        self.window.cookies = [jar("web_session=logged-in", httponly=True)]
        self.until(lambda: self.controller.state()["status"] == "success")

    def test_detects_session_changed_before_login_modal_disappears(self):
        self.controller.start()
        self.until(lambda: self.window.cookie_reads > 0)
        self.window.cookies = [jar("web_session=logged-in", httponly=True)]
        previous_reads = self.window.cookie_reads
        self.until(lambda: self.window.cookie_reads > previous_reads)
        self.assertEqual(self.controller.state()["status"], "waiting")
        self.window.page = {"authenticated": False, "login_visible": False, "qr_visible": False}
        self.until(lambda: self.controller.state()["status"] == "success")
        self.assertIn("web_session=logged-in", self.controller.state()["cookie"])

    def test_temporary_navigation_error_does_not_abort_login(self):
        original = self.window.evaluate_js
        calls = []

        def evaluate(script):
            calls.append(True)
            if len(calls) == 1:
                raise RuntimeError("Navigation in progress")
            return original(script)

        self.window.evaluate_js = evaluate
        self.window.cookies = [jar("web_session=logged-in", httponly=True)]
        self.window.page = {"authenticated": True}
        self.controller.start()
        self.until(lambda: self.controller.state()["status"] == "success")
        self.assertGreaterEqual(len(calls), 2)

    def test_native_read_does_not_wait_for_the_page_js_bridge_loaded_event(self):
        self.window.events.loaded.clear()
        with patch("source.GUI.login.uses_native_webview", return_value=True), patch(
            "source.GUI.login.read_login_url", return_value=self.window.url
        ), patch("source.GUI.login.read_login_cookies", return_value=[jar("web_session=native", httponly=True)]), patch(
            "source.GUI.login.read_login_state", return_value={"authenticated": True}
        ):
            self.controller.start()
            self.until(lambda: self.controller.state()["status"] == "success")
        self.assertIn("web_session=native", self.controller.state()["cookie"])

    def test_duplicate_click_reuses_window_and_closed_window_can_retry(self):
        self.controller.start()
        self.controller.start()
        self.assertEqual(self.factory.call_count, 1)
        self.assertEqual(self.window.shown, 1)
        self.window.destroy()
        self.assertEqual(self.controller.state()["status"], "cancelled")
        replacement = LoginWindow()
        self.factory.return_value = replacement
        self.controller.start()
        self.assertEqual(self.factory.call_count, 2)
        self.assertEqual(self.controller.state()["status"], "waiting")

    def test_redirect_to_unrelated_origin_never_reads_cookies(self):
        self.window.url = "https://www.xiaohongshu.com.example.org/"
        self.controller.start()
        time.sleep(0.05)
        self.assertEqual(self.window.cookie_reads, 0)
        self.assertNotIn("cookie", self.controller.state())

    def test_site_error_is_reported_without_reading_cookies(self):
        self.window.url = "https://www.xiaohongshu.com/website-login/error?error_msg=Network%20unavailable"
        self.controller.start()
        self.until(lambda: self.controller.state()["status"] == "error")
        self.assertEqual(self.controller.state()["message"], "Network unavailable")
        self.assertEqual(self.window.cookie_reads, 0)

    def test_timeout_preserves_window_for_explicit_cookie_read(self):
        self.controller._timeout = 0.04
        self.controller.start()
        self.until(lambda: self.controller.state()["status"] == "error")
        self.assertFalse(self.window.closed)
        self.assertNotIn("cookie", self.controller.state())
        self.window.cookies = [jar("web_session=confirmed", httponly=True)]
        self.assertEqual(self.controller.capture()["status"], "success")

    def test_manual_capture_does_not_depend_on_page_detection(self):
        self.window.evaluate_js = lambda _: (_ for _ in ()).throw(RuntimeError("blocked"))
        self.controller.start()
        self.until(lambda: self.window.cookie_reads > 1)
        self.window.cookies = [jar("web_session=confirmed", httponly=True)]
        self.assertEqual(self.controller.capture()["status"], "success")
        self.assertIn("web_session=confirmed", self.controller.state()["cookie"])

    def test_manual_capture_rejects_missing_session_or_wrong_origin(self):
        self.controller.start()
        self.window.cookies = [jar("a1=visitor")]
        self.assertEqual(self.controller.capture()["status"], "error")
        self.assertFalse(self.window.closed)
        self.window.url = "https://example.com"
        self.window.cookies = [jar("web_session=confirmed")]
        self.assertEqual(self.controller.capture()["status"], "error")
        self.assertNotIn("cookie", self.controller.state())

    def test_explicit_capture_after_window_close_uses_last_observed_session(self):
        delivered = []
        self.controller._on_success = delivered.append
        self.window.cookies = [jar("web_session=last-session", httponly=True)]
        self.controller.start()
        self.until(lambda: self.controller.state()["can_capture"] and self.window.cookie_reads > 1)
        self.window.destroy()
        self.assertEqual(self.controller.state()["status"], "cancelled")
        self.assertNotIn("cookie", self.controller.state())
        self.assertTrue(self.controller.state()["can_capture"])
        self.assertEqual(self.controller.capture()["status"], "success")
        self.assertIn("web_session=last-session", delivered[0])

    def test_restart_cannot_import_previous_windows_cached_cookie(self):
        self.controller.start()
        self.until(lambda: self.window.cookie_reads > 1)
        self.window.destroy()
        replacement = LoginWindow()
        replacement.events.loaded.clear()
        self.factory.return_value = replacement
        self.controller.start()
        self.assertFalse(self.controller._last_cookies)

    def test_unchanged_session_is_read_when_page_confirms_login(self):
        self.controller.start()
        self.until(lambda: self.window.cookie_reads > 0)
        self.window.page = {"login_visible": False, "authenticated": True}
        self.until(lambda: self.controller.state()["status"] == "success")

    def test_success_push_and_diagnostics_do_not_expose_cookie_values(self):
        with TemporaryDirectory() as directory:
            self.controller._diagnostic_path = Path(directory) / "qr.log"
            delivered = []
            self.controller._on_success = delivered.append
            self.controller.start()
            self.until(lambda: self.window.cookie_reads > 0)
            self.window.cookies = [jar("web_session=sensitive-session", httponly=True)]
            self.controller.capture()
            self.controller.confirm_import()
            self.assertEqual(len(delivered), 1)
            text = self.controller._diagnostic_path.read_text(encoding="utf-8")
            self.assertNotIn("sensitive-session", text)
            self.assertIn("cookie_filled_in_settings", text)
            self.controller.close()
            self.controller._diagnostic_path = None

    def test_cookie_domains_and_quoted_values(self):
        values = collect_login_cookies([
            jar('token="a;b"'),
            jar("foreign=1", "evilxiaohongshu.com"),
            jar("foreign2=1", "xiaohongshu.com.example.org"),
        ])
        self.assertEqual(list(values), ["token"])
        self.assertEqual(values["token"].coded_value, '"a;b"')
        self.assertTrue(is_login_origin("https://www.xiaohongshu.com/explore"))
        self.assertFalse(is_login_origin("http://www.xiaohongshu.com/explore"))


if __name__ == "__main__":
    unittest.main()

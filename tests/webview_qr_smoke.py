"""Windows WebView2 smoke: the real settings UI, native bridge and HttpOnly jar.

Run with the project's venv. Uses only localhost and temporary settings.
"""

import json
import sys
import threading
import time
from contextlib import suppress
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import webview

from source.GUI import backend as backend_module, login
from source.GUI.backend import GuiApi, GuiBackend
from source.module import ROOT, Settings


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        manual = self.path.startswith(("/manual", "/closed"))
        script = (
            "Object.defineProperty(window,'__INITIAL_STATE__',{get(){throw Error('unreadable state')}});"
            if manual else
            "window.__INITIAL_STATE__={user:{userInfo:{_rawValue:{guest:false}}}};"
        )
        if self.path.startswith("/broken-bridge"):
            script += "window.pywebview.stringify=()=>null;"
        html = ("<!doctype html><body><div id='login-parent'><div class='login-container'><div class='container'>"
                "<img width='180' height='180'></div></div></div><script>"
                "setTimeout(()=>{document.getElementById('login-parent').style.opacity='0';"
                + script + "},900);</script>").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        # Deliberately stable across login, and inaccessible to document.cookie.
        self.send_header("Set-Cookie", "web_session=stable-test-session; Path=/; HttpOnly")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)


class TestBackend(GuiBackend):
    async def _initialize(self):
        self.settings = self.settings_manager.run()
        self.settings["disclaimer_accepted"] = True


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    login.is_login_origin = lambda url: url.startswith(base + "/")
    login.collect_login_cookies = lambda jars: {name: value for jar in jars for name, value in jar.items()}
    outcomes = []
    with TemporaryDirectory() as directory:
        backend_module.VOLUME = Path(directory)
        backend = TestBackend()
        backend.settings_manager = Settings(Path(directory))
        api = GuiApi(backend)
        api._qr_login._diagnostic_path = Path(directory) / "diagnostic.log"
        api._qr_login._poll_interval = 0.15
        window = webview.create_window("QR bridge smoke", (ROOT / "static/GUI/index.html").as_uri(),
                                       js_api=api, hidden=True, width=1280, height=720)
        api._bind_window(window)
        create = webview.create_window

        def hidden_window(*args, **kwargs):
            kwargs["hidden"] = True
            return create(*args, **kwargs)

        webview.create_window = hidden_window
        backend.start()

        def until(predicate, seconds=12):
            end = time.monotonic() + seconds
            while time.monotonic() < end:
                if predicate():
                    return
                time.sleep(0.1)
            raise AssertionError("UI transition timed out")

        def run():
            try:
                until(lambda: window.events.loaded.is_set())
                until(lambda: window.evaluate_js("document.getElementById('startupScreen').hidden"))
                window.evaluate_js("document.querySelector('[data-view=settings]').click()")
                for case in ("auto", "broken-bridge", "manual", "closed"):
                    login.LOGIN_URL = base + "/" + case
                    window.evaluate_js("document.getElementById('settingsCookie').value='';document.getElementById('cookieQrLogin').click()")
                    if case in {"manual", "closed"}:
                        previous_errors = (Path(directory) / "diagnostic.log").read_text().count('page_detection_failed') if (Path(directory) / "diagnostic.log").exists() else 0
                        until(lambda: (Path(directory) / "diagnostic.log").exists()
                              and (Path(directory) / "diagnostic.log").read_text().count('page_detection_failed') > previous_errors)
                        if case == "closed":
                            api._qr_login._window.destroy()
                            until(lambda: api._qr_login.state()["status"] == "cancelled")
                            until(lambda: not window.evaluate_js("document.getElementById('cookieReadLogin').disabled"))
                        window.evaluate_js("document.getElementById('cookieReadLogin').click()")
                    until(lambda: window.evaluate_js("document.getElementById('settingsCookie').value.includes('web_session=stable-test-session')"))
                    until(lambda: 'cookie_filled_in_settings' in (Path(directory) / "diagnostic.log").read_text())
                    if case == "auto":
                        observations = [json.loads(line) for line in (Path(directory) / "diagnostic.log").read_text().splitlines()]
                        assert any(item.get("authenticated") is True and item.get("login_visible") is False
                                   and item.get("qr_visible") is False for item in observations)
                    outcomes.append(case + ": PASS")
                diagnostic = (Path(directory) / "diagnostic.log").read_text()
                assert "stable-test-session" not in diagnostic
                assert diagnostic.count('"event": "cookie_filled_in_settings"') == 4
                assert '"native_browser": true' in diagnostic
            except Exception as error:
                outcomes.append("FAIL: " + str(error))
                with suppress(Exception):
                    print("DIAGNOSTICS:", (Path(directory) / "diagnostic.log").read_text())
            finally:
                api._close_qr_login()
                window.destroy()

        try:
            webview.start(run)
        finally:
            backend.stop()
            server.shutdown()
    print(json.dumps(outcomes))
    return 0 if outcomes == ["auto: PASS", "broken-bridge: PASS", "manual: PASS", "closed: PASS"] else 1


if __name__ == "__main__":
    sys.exit(main())

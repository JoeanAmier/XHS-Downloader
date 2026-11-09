"""Read only the dedicated login WebView, without the website's JS bridge."""

from http.cookies import SimpleCookie
from json import dumps, loads
from threading import Event


def uses_native_webview(window) -> bool:
    return getattr(getattr(window, "gui", None), "renderer", None) == "edgechromium"


def _devtools(window, method: str, parameters: dict, timeout: float = 5) -> dict:
    # Import after pywebview has initialized pythonnet and WebView2. No
    # debugging port is opened; calls remain inside this window's control.
    from System import Action, String
    from System.Threading.Tasks import Task

    complete = Event()
    response = {}

    def done(task):
        try:
            response["value"] = str(task.Result)
        except Exception:
            response["failed"] = True
        finally:
            complete.set()

    def begin():
        try:
            view = window.native.webview
            task = view.CoreWebView2.CallDevToolsProtocolMethodAsync(method, dumps(parameters))
            task.ContinueWith(Action[Task[String]](done))
        except Exception:
            response["failed"] = True
            complete.set()

    window.native.BeginInvoke(Action(begin))
    if not complete.wait(timeout):
        raise TimeoutError("Login browser operation timed out")
    if response.get("failed"):
        raise RuntimeError("Login browser operation failed")
    value = loads(response["value"])
    if "error" in value or "exceptionDetails" in value:
        raise RuntimeError("Login browser evaluation failed")
    return value


def _evaluate(window, expression: str):
    value = _devtools(window, "Runtime.evaluate", {
        "expression": expression,
        "returnByValue": True,
        "timeout": 3000,
    })
    return value.get("result", {}).get("value")


def read_login_url(window) -> str:
    if uses_native_webview(window):
        return _evaluate(window, "location.href") or ""
    return window.get_current_url() or ""


def read_login_cookies(window, url: str) -> list[SimpleCookie]:
    if not uses_native_webview(window):
        return window.get_cookies() or []
    # Network.getCookies returns HttpOnly cookies as well and scopes the
    # query to the checked login URL, rather than every profile's cookies.
    cookies = _devtools(window, "Network.getCookies", {"urls": [url]}).get("cookies", [])
    jars = []
    for value in cookies:
        jar = SimpleCookie()
        name = value["name"]
        jar[name] = value["value"]
        jar[name]["domain"] = value.get("domain", "")
        jar[name]["path"] = value.get("path", "/")
        jar[name]["httponly"] = value.get("httpOnly", False)
        jars.append(jar)
    return jars


def read_login_state(window, script: str) -> dict:
    if uses_native_webview(window):
        value = _evaluate(window, script)
    else:
        value = window.evaluate_js(script)
    return value if isinstance(value, dict) else {}

from json import JSONDecodeError, loads
from re import IGNORECASE, search
from urllib.parse import parse_qs, urlsplit


class RiskControlError(Exception):
    pass


def check_risk_payload(payload) -> None:
    if not isinstance(payload, dict):
        return
    code = str(payload.get("code", ""))
    message = str(payload.get("msg") or payload.get("message") or payload.get("error_msg") or "").lower()
    indicators = ("风控", "风险", "账号异常", "账号存在异常", "访问频繁", "请求频繁", "操作频繁", "过于频繁", "安全验证", "人机验证", "captcha", "rate limit", "too many requests")
    if code in {"300011", "300012", "461", "471", "-10000"} or (
        (payload.get("success") is False or code not in {"", "0", "200"})
        and any(indicator in message for indicator in indicators)
    ):
        raise RiskControlError()


def check_risk_response(response, *, inspect_body: bool = True) -> None:
    if response.status_code in {429, 461, 471}:
        raise RiskControlError()

    parts = urlsplit(str(response.url or ""))
    host = (parts.hostname or "").lower()
    if host == "xiaohongshu.com" or host.endswith(".xiaohongshu.com"):
        query = parse_qs(parts.query)
        if parts.path.startswith(("/website-login/captcha", "/website-login/verify")):
            raise RiskControlError()
        if any(code in {"300011", "300012", "461", "471", "-10000"} for code in query.get("error_code", [])):
            raise RiskControlError()

    if inspect_body:
        check_risk_body(response.text or "")


def check_risk_body(text: str) -> None:
    stripped = text.lstrip()
    if stripped.startswith("{"):
        try:
            check_risk_payload(loads(stripped))
        except JSONDecodeError:
            pass
    else:
        title = search(r"<title[^>]*>\s*(.*?)\s*</title>", text[:8192], IGNORECASE)
        if title and title.group(1).strip().lower() in {"安全验证", "安全验证 - 小红书", "security verification"}:
            raise RiskControlError()

"""User-owned HMAC token generation and validation."""

from base64 import urlsafe_b64decode, urlsafe_b64encode
from binascii import Error as Base64Error
from hashlib import sha256
from hmac import compare_digest, new
from json import dumps, loads
from secrets import token_bytes
from time import time

from .static import VOLUME

_TOKEN_LIFETIME: int | None = None
_PROJECT_ID = "JoeanAmier/XHS-Downloader"
_SECRET_KEY_PATH = VOLUME / "auth_secret.key"


def _encode(value: bytes) -> str:
    return urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _decode(value: str) -> bytes:
    return urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _load_secret() -> bytes:
    if not _SECRET_KEY_PATH.is_file():
        secret = token_bytes(32)
        _SECRET_KEY_PATH.write_bytes(secret)
    return _SECRET_KEY_PATH.read_bytes()


def generate_auth_token() -> str:
    """Create a token authenticated by the user's local secret key."""

    payload = dumps(
        {
            "create_time": int(time()),
            "project_id": _PROJECT_ID,
        },
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    encoded_payload = _encode(payload)
    signature = new(_load_secret(), payload, sha256).digest()
    return f"{encoded_payload}.{_encode(signature)}"


def verify_auth_token(token: str | None) -> bool:
    """Return whether a token has a valid signature and is not expired."""

    if not isinstance(token, str) or not token:
        return False
    try:
        encoded_payload, encoded_signature = token.split(".", 1)
        payload = _decode(encoded_payload)
        signature = _decode(encoded_signature)
        expected_signature = new(_load_secret(), payload, sha256).digest()
        if not compare_digest(signature, expected_signature):
            return False
        data = loads(payload)
        create_time = data["create_time"]
        return data["project_id"] == _PROJECT_ID and (
            _TOKEN_LIFETIME is None
            or create_time <= time() < create_time + _TOKEN_LIFETIME
        )
    except (
        AttributeError,
        Base64Error,
        KeyError,
        TypeError,
        ValueError,
        UnicodeDecodeError,
    ):
        return False


__all__ = ["generate_auth_token", "verify_auth_token"]

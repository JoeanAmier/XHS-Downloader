from pathlib import Path


class Settings:
    path = Path("./settings.json")
    default = {
        "path": "./",
        "folder": "Download",
        "user-agent": None,
        "proxies": None,
        "timeout": 10,
        "chunk": 256 * 1024,
    }

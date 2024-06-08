from pathlib import Path

__all__ = [
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_BETA",
    "ROOT",
    "REPOSITORY",
    "LICENCE",
    "RELEASES",
    "MASTER",
    "PROMPT",
    "GENERAL",
    "PROGRESS",
    "ERROR",
    "WARNING",
    "INFO",
    "USERSCRIPT",
    "HEADERS",
    "PROJECT",
]

VERSION_MAJOR = 2
VERSION_MINOR = 0
VERSION_BETA = True
ROOT = Path(__file__).resolve().parent.parent.parent
PROJECT = f"XHS-Downloader V{VERSION_MAJOR}.{
VERSION_MINOR}{" Beta" if VERSION_BETA else ""}"

REPOSITORY = "https://github.com/JoeanAmier/XHS-Downloader"
LICENCE = "GNU General Public License v3.0"
RELEASES = "https://github.com/JoeanAmier/XHS-Downloader/releases/latest"

USERSCRIPT = "https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js"

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-SG,zh-CN;q=0.9,zh;q=0.8',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 '
                  'Safari/537.36',
}

MASTER = "b #fff200"
PROMPT = "b turquoise2"
GENERAL = "b bright_white"
PROGRESS = "b bright_magenta"
ERROR = "b bright_red"
WARNING = "b bright_yellow"
INFO = "b bright_green"

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
    "USERAGENT",
    "COOKIE",
]

VERSION_MAJOR = 1
VERSION_MINOR = 8
VERSION_BETA = True
ROOT = Path(__file__).resolve().parent.parent.parent

REPOSITORY = "https://github.com/JoeanAmier/XHS-Downloader"
LICENCE = "GNU General Public License v3.0"
RELEASES = "https://github.com/JoeanAmier/XHS-Downloader/releases/latest"

USERSCRIPT = "https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js"

USERAGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
    "Safari/537.36")
COOKIE = (
    "abRequestId=54c534bb-a2c6-558f-8e03-5b4c5c45635c; xsecappid=xhs-pc-web; a1=18c286a400"
    "4jy56qvzejvp631col0hd3032h4zjez50000106381; webId=779c977da3a15b5623015be94bdcc9e9; g"
    "id=yYSJYK0qDW8KyYSJYK048quV84Vv2KAhudVhJduUKqySlx2818xfq4888y8KqYy8y2y2f8Jy; web_sess"
    "ion=030037a259ce5f15c8d560dc12224a9fdc2ed1; webBuild=3.19.4; websectiga=984412fef754c"
    "018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; sec_poison_id=3dd48845-d604-4535"
    "-bcc2-a859e97518bf; unread={%22ub%22:%22655eb3d60000000032033955%22%2C%22ue%22:%22656"
    "e9ef2000000003801ff3d%22%2C%22uc%22:29}; cache_feeds=[]")

MASTER = "b #fff200"
PROMPT = "b turquoise2"
GENERAL = "b bright_white"
PROGRESS = "b bright_magenta"
ERROR = "b bright_red"
WARNING = "b bright_yellow"
INFO = "b bright_green"

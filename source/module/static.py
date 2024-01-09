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
    "HEADERS",
]

VERSION_MAJOR = 1
VERSION_MINOR = 8
VERSION_BETA = True
ROOT = Path(__file__).resolve().parent.parent.parent

REPOSITORY = "https://github.com/JoeanAmier/XHS-Downloader"
LICENCE = "GNU General Public License v3.0"
RELEASES = "https://github.com/JoeanAmier/XHS-Downloader/releases/latest"

USERSCRIPT = "https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Dnt": "1",
    "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}
USERAGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
    "Safari/537.36 Edg/120.0.0.0")
COOKIE = (
    "abRequestId=a1c55c3d-edcd-5753-938b-15d22a78cb8a; webBuild=3.23.2; "
    "a1=18ceecc41c5d2gkprctahn1jayh458m5eoos9grxb50000267832; webId=79879aaf1b46fa2120dfba20d6155928; "
    "websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; "
    "sec_poison_id=52bff38d-96eb-40b6-a46b-5e7cc86014e4; web_session=030037a2ae3713ec49882425e5224a3cbb4eef; "
    "gid=yYSddSS2DKdyyYSddSS4ylkFS2fJkTUFS90xlCDIyV0vxM2842Y62j888JKWYqJ8iDD4KY2d; xsecappid=xhs-pc-web")

MASTER = "b #fff200"
PROMPT = "b turquoise2"
GENERAL = "b bright_white"
PROGRESS = "b bright_magenta"
ERROR = "b bright_red"
WARNING = "b bright_yellow"
INFO = "b bright_green"

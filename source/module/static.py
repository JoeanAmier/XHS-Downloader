from pathlib import Path

VERSION_MAJOR = 2
VERSION_MINOR = 3
VERSION_BETA = True
ROOT = Path(__file__).resolve().parent.parent.parent
PROJECT = f"XHS-Downloader V{VERSION_MAJOR}.{
VERSION_MINOR}{" Beta" if VERSION_BETA else ""}"

REPOSITORY = "https://github.com/JoeanAmier/XHS-Downloader"
LICENCE = "GNU General Public License v3.0"
RELEASES = "https://github.com/JoeanAmier/XHS-Downloader/releases/latest"

USERSCRIPT = "https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js"

USERAGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 '
             'Safari/537.36 Edg/128.0.0.0')
SEC_CH_UA = '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"'
SEC_CH_UA_PLATFORM = '"Windows"'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'dnt': '1',
    'pragma': 'no-cache',
    # 'priority': 'u=0, i',
    # 'sec-ch-ua': SEC_CH_UA,
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': SEC_CH_UA_PLATFORM,
    # 'sec-fetch-dest': 'document',
    # 'sec-fetch-mode': 'navigate',
    # 'sec-fetch-site': 'none',
    # 'sec-fetch-user': '?1',
    # 'upgrade-insecure-requests': '1',
    'user-agent': USERAGENT,
}

MASTER = "b #fff200"
PROMPT = "b turquoise2"
GENERAL = "b bright_white"
PROGRESS = "b bright_magenta"
ERROR = "b bright_red"
WARNING = "b bright_yellow"
INFO = "b bright_green"

FILE_SIGNATURES: tuple[tuple[int, bytes, str,], ...] = (
    # 分别为偏移量(字节)、十六进制签名、后缀
    # 参考：https://en.wikipedia.org/wiki/List_of_file_signatures
    # 参考：https://www.garykessler.net/library/file_sigs.html
    (0, b"\xFF\xD8\xFF", "jpeg"),
    (0, b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A", "png"),
    (4, b"\x66\x74\x79\x70\x61\x76\x69\x66", "avif"),
    (4, b"\x66\x74\x79\x70\x68\x65\x69\x63", "heic"),
    (8, b"\x57\x45\x42\x50", "webp"),
    (4, b"\x66\x74\x79\x70\x4D\x53\x4E\x56", "mp4"),
    (4, b"\x66\x74\x79\x70\x69\x73\x6F\x6D", "mp4"),
    (4, b"\x66\x74\x79\x70\x6D\x70\x34\x32", "m4v"),
    (4, b"\x66\x74\x79\x70\x71\x74\x20\x20", "mov"),
    (0, b"\x1A\x45\xDF\xA3", "mkv"),
    (0, b"\x00\x00\x01\xB3", "mpg"),
    (0, b"\x00\x00\x01\xBA", "mpg"),
    (0, b"\x46\x4c\x56\x01", "flv"),
    (8, b"\x41\x56\x49\x20", "avi"),
)
FILE_SIGNATURES_LENGTH = max(offset + len(signature) for offset, signature, _ in FILE_SIGNATURES)

MAX_WORKERS: int = 3

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
    "DISCLAIMER_TEXT",
    "USERSCRIPT",
    "USERAGENT",
    "COOKIE",
]

VERSION_MAJOR = 1
VERSION_MINOR = 8
VERSION_BETA = True
ROOT = Path(__file__).resolve().parent.parent

REPOSITORY = "https://github.com/JoeanAmier/XHS-Downloader"
LICENCE = "GNU General Public License v3.0"
RELEASES = "https://github.com/JoeanAmier/XHS-Downloader/releases/latest"
DISCLAIMER_TEXT = (
    "关于 XHS-Downloader 的 免责声明：",
    "",
    "1. 使用者对本项目的使用由使用者自行决定，并自行承担风险。作者对使用者使用本项目所产生的任何损失、责任、或风险概不负责。",
    "2. 本项目的作者提供的代码和功能是基于现有知识和技术的开发成果。作者尽力确保代码的正确性和安全性，但不保证代码完全没有错误或缺陷。",
    "3. 使用者在使用本项目时必须严格遵守 GNU General Public License v3.0 的要求，并在适当的地方注明使用了 GNU General Public License v3.0 的代码。",
    "4. 使用者在任何情况下均不得将本项目的作者、贡献者或其他相关方与使用者的使用行为联系起来，或要求其对使用者使用本项目所产生的任何损失或损害负责。",
    "5. 使用者在使用本项目的代码和功能时，必须自行研究相关法律法规，并确保其使用行为合法合规。任何因违反法律法规而导致的法律责任和风险，均由使用者自行承担。",
    "6. 本项目的作者不会提供 XHS-Downloader 项目的付费版本，也不会提供与 XHS-Downloader 项目相关的任何商业服务。",
    "7. 基于本项目进行的任何二次开发、修改或编译的程序与原创作者无关，原创作者不承担与二次开发行为或其结果相关的任何责任，使用者应自行对因"
    "二次开发可能带来的各种情况负全部责任。",
    "",
    "在使用本项目的代码和功能之前，请您认真考虑并接受以上免责声明。如果您对上述声明有任何疑问或不同意，请不要使用本项目的代码和功能。如果"
    "您使用了本项目的代码和功能，则视为您已完全理解并接受上述免责声明，并自愿承担使用本项目的一切风险和后果。",
    "",
    ">" * 50,
)

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

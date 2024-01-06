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
DISCLAIMER_TEXT_ENG = (
    "Disclaimer about XHS-Downloader:",
    "",
    "1. The use of the Program by the User is at the user's own discretion and risk. The author shall not be liable for any loss, liability, or risk arising from the use of this project.",
    "2. The code and functionality provided by the authors of this project are based on the development of existing knowledge and technology. The author makes every effort to ensure the correctness and security of the code, but does not guarantee that the code is completely free of errors or defects.",
    "3. Users must strictly comply with the requirements of the GNU General Public License v3.0 when using the Project, and indicate the use of the GNU General Public License v3.0 code where appropriate.",
    "4. Under no circumstances shall the authors, contributors or other parties involved in the Project be associated with the User's use of the Project, or hold them liable for any loss or damage arising from the User's use of the Project.",
    "5. When using the code and functions of this project, users must study the relevant laws and regulations on their own and ensure that their use is legal and compliant. Any legal liabilities and risks caused by violations of laws and regulations shall be borne by the user.",
    "6. The authors of this project will not provide a paid version of the XHS-Downloader project, nor will they provide any commercial services related to the XHS-Downloader project.",
    "7. Any secondary development, modification or compilation of programs based on this project has nothing to do with the original creator, and the original creator does not assume any responsibility related to the secondary development behavior or its results, and the user shall be fully responsible for the various situations that may be brought about by the secondary development.",
    "",
    "Before using the code and functions of this project, please carefully consider and accept the above disclaimer. If you have any questions or disagree with the above statement, please do not use the code and features of this project. If you use the code and functions of this project, it is deemed that you have fully understood and accepted the above disclaimer and voluntarily assume all risks and consequences of using this project.",
    "",
    ">" * 50,
)

USERSCRIPT = "https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js"

MASTER = "b #fff200"
PROMPT = "b turquoise2"
GENERAL = "b bright_white"
PROGRESS = "b bright_magenta"
ERROR = "b bright_red"
WARNING = "b bright_yellow"
INFO = "b bright_green"

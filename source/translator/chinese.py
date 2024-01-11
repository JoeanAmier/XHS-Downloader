__all__ = ["Chinese"]


class Chinese:
    code: str = "zh-CN"
    disclaimer: tuple[str] = (
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

    download_link_error: str = "提取作品文件下载地址失败！"
    extract_link_failure: str = "提取小红书作品链接失败！"
    invalid_link: str = "未输入任何小红书作品链接！"
    download_failure: str = "下载小红书作品文件失败！"
    check_update_notification: str = "正在检查新版本，请稍等..."
    development_version_update: str = "当前版本为开发版, 可更新至正式版！"
    latest_development_version: str = "当前已是最新开发版！"
    latest_official_version: str = "当前已是最新正式版！"
    check_update_failure: str = "检测新版本失败！"

    open_source_protocol: str = "开源协议："
    project_address: str = "项目地址："
    input_box_title: str = "请输入小红书图文/视频作品链接："
    input_prompt: str = "多个链接之间使用空格分隔"
    download_button: str = "下载无水印图片/视频"
    paste_button: str = "读取剪贴板"
    reset_button: str = "清空输入框"

    exit_program: str = "退出程序"
    check_updates: str = "检查更新"
    get_script: str = "获取脚本"
    choose_language: str = "选择语言"

    @staticmethod
    def request_error(url: str) -> str:
        return f"网络异常，请求 {url} 失败！"

    @staticmethod
    def skip_download(name: str) -> str:
        return f"{name} 已存在，跳过下载！"

    @staticmethod
    def download_success(name: str) -> str:
        return f"{name} 下载成功！"

    @staticmethod
    def download_error(name: str) -> str:
        return f"网络异常，{name} 下载失败！"

    @staticmethod
    def pending_processing(num: int) -> str:
        return f"共 {num} 个小红书作品待处理..."

    @staticmethod
    def start_processing(url: str) -> str:
        return f"开始处理作品：{url}"

    @staticmethod
    def get_data_failure(url: str) -> str:
        return f"{url} 获取数据失败！"

    @staticmethod
    def extract_data_failure(url: str) -> str:
        return f"{url} 提取数据失败！"

    @staticmethod
    def processing_completed(url: str) -> str:
        return f"作品处理完成：{url}"

    @staticmethod
    def official_version_update(major: int, minor: int) -> str:
        return f"检测到新版本：{major}.{minor}"

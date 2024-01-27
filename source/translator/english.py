from .chinese import Chinese

__all__ = ["English"]


class English(Chinese):
    code: str = "en-GB"
    disclaimer: tuple[str] = (
        "Disclaimer about XHS-Downloader:",
        "",
        "1. The user decides on their own use of this project and assumes all risks. The author is not responsible "
        "for any losses, liabilities, or risks incurred by the user in using this project.",
        "2. The code and features provided by the author of this project are developed based on existing knowledge "
        "and technology. The author strives to ensure the correctness and security of the code but does not guarantee "
        "that the code is entirely free of errors or defects.",
        "3. The user must strictly adhere to the requirements of the GNU General Public License v3.0 when using this "
        "project and appropriately acknowledge the use of code licensed under the GNU General Public License v3.0.",
        "4. Under no circumstances may the user associate the author, contributors, or other relevant parties of this "
        "project with the user's actions, nor demand them to be held responsible for any losses or damages incurred "
        "by the user in using this project.",
        "5. The user must independently research relevant laws and regulations when using the code and features of "
        "this project, ensuring that their use is legal and compliant. Any legal responsibilities and risks arising "
        "from violations of laws and regulations are the sole responsibility of the user.",
        "6. The author of this project will not offer a paid version of the XHS-Downloader project and will not "
        "provide any commercial services related to the XHS-Downloader project.",
        "7. Any secondary development, modification, or compilation of programs based on this project is not "
        "associated with the original author. The original author is not responsible for any consequences related to "
        "secondary development actions or their results. The user is solely responsible for all situations that may "
        "arise from secondary development.",
        "",
        "Before using the code and features of this project, please carefully consider and accept the above "
        "disclaimers. If you have any questions or do not agree with the statements above, please refrain from using "
        "the code and features of this project. If you proceed to use the code and features of this project, "
        "it will be considered that you fully understand and accept the disclaimers mentioned above, and willingly "
        "assume all risks and consequences associated with using this project.",
        "",
        ">" * 50,
    )

    download_link_error: str = "Failed to extract the download address for the Xiaohongshu works files!"
    extract_link_failure: str = "Failed to extract the links for Xiaohongshu works!"
    invalid_link: str = "No Xiaohongshu works links provided!"
    download_failure: str = "Failed to download the Xiaohongshu works files!"
    check_update_notification: str = "Checking for new version, please wait..."
    development_version_update: str = (
        "The current version is a development version, and can be updated to the "
        "official version!")
    latest_development_version: str = "You are already using the latest development version!"
    latest_official_version: str = "You are already using the latest official version!"
    check_update_failure: str = "Failed to check for a new version!"

    open_source_protocol: str = "Open Source License:"
    project_address: str = "Project Address:"
    input_box_title: str = "Please enter the link to the Xiaohongshu image/text or video works:"
    input_prompt: str = "Separate multiple links with spaces"
    download_button: str = "Download images/video files"
    paste_button: str = "Read the clipboard"
    reset_button: str = "Clear the input box"

    exit_program: str = "Exit the program"
    check_updates: str = "Check for updates"
    get_script: str = "Get the script"
    settings: str = "Settings"

    work_path: str = "Work path:"
    folder_name: str = "Folder name:"
    user_agent: str = "User-Agent:"
    cookie: str = "Cookie:"
    proxy: str = "Network proxy:"
    timeout: str = "Request timeout limit:"
    chunk: str = "Download data block size:"
    max_retry: str = "Maximum retry attempts:"
    record_data: str = "Record works data"
    image_format: str = "Image download format"
    folder_mode: str = "Folder archiving mode"
    language: str = "Program language"
    server: str = "Start local server"

    work_path_placeholder: str = "Program root path"
    user_agent_placeholder: str = "Default UA"
    cookie_placeholder_true: str = "Xiaohongshu web version cookie, no login required, parameters have been set"
    cookie_placeholder_false: str = "Xiaohongshu web version cookie, no login required, parameters not set"
    proxy_placeholder: str = "No proxy"

    settings_title: str = "Settings"
    save_button: str = "Save configuration"
    abandon_button: str = "Discard changes"

    processing: str = "Processing..."

    monitor_mode: str = "Currently in monitoring clipboard mode"
    monitor_text: str = (
        "The program will automatically read and extract the link to Xiaohongshu's works from the "
        "clipboard, and automatically download the corresponding work file. If you want to close it, "
        "please click the close button or write the \"close\" text to the clipboard!")
    close_monitor: str = "Exit monitoring clipboard mode"

    @staticmethod
    def request_error(url: str) -> str:
        return f"Network error, failed to access {url}!"

    @staticmethod
    def skip_download(name: str) -> str:
        return f"{name} already exists, skipping download!"

    @staticmethod
    def download_success(name: str) -> str:
        return f"{name} download successful!"

    @staticmethod
    def download_error(name: str) -> str:
        return f"Network error, {name} download failed!"

    @staticmethod
    def pending_processing(num: int) -> str:
        return f"{num} works from Xiaohongshu are awaiting processing..."

    @staticmethod
    def start_processing(url: str) -> str:
        return f"Start processing the works: {url}"

    @staticmethod
    def get_data_failure(url: str) -> str:
        return f"{url} failed to retrieve data!"

    @staticmethod
    def extract_data_failure(url: str) -> str:
        return f"{url} failed to extract data!"

    @staticmethod
    def processing_completed(url: str) -> str:
        return f"works processing completed: {url}"

    @staticmethod
    def official_version_update(major: int, minor: int) -> str:
        return f"New version detected: {major}.{minor}"

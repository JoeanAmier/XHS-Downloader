__all__ = ["Language"]


class Language:
    code: str = None
    disclaimer: tuple[str] = None

    download_link_error: str = None
    extract_link_failure: str = None
    invalid_link: str = None
    download_failure: str = None
    check_update_notification: str = None
    development_version_update: str = None
    latest_development_version: str = None
    latest_official_version: str = None
    check_update_failure: str = None

    open_source_protocol: str = None
    project_address: str = None
    input_box_title: str = None
    input_prompt: str = None
    download_button: str = None
    paste_button: str = None
    reset_button: str = None

    exit_program: str = None
    check_updates: str = None
    get_script: str = None
    choose_language: str = None

    @staticmethod
    def request_error(url: str) -> str:
        pass

    @staticmethod
    def skip_download(name: str) -> str:
        pass

    @staticmethod
    def download_success(name: str) -> str:
        pass

    @staticmethod
    def download_error(name: str) -> str:
        pass

    @staticmethod
    def pending_processing(num: int) -> str:
        pass

    @staticmethod
    def start_processing(url: str) -> str:
        pass

    @staticmethod
    def get_data_failure(url: str) -> str:
        pass

    @staticmethod
    def extract_data_failure(url: str) -> str:
        pass

    @staticmethod
    def processing_completed(url: str) -> str:
        pass

    @staticmethod
    def official_version_update(major: int, minor: int) -> str:
        pass

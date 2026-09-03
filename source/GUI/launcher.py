"""启动 GUI 及其 PyWebView 下载器桥接。"""

import sys
from pathlib import Path

import webview

from ..module import PROJECT, ROOT
from .backend import GuiApi, GuiBackend

# GUI 静态资源与 Python 桥接代码分离，统一从项目 static 目录加载。
INDEX_PATH = ROOT.joinpath("static", "GUI", "index.html")


def get_index_path() -> Path:
    """返回 GUI 入口页面的绝对路径，并在文件缺失时尽早报错。"""

    if not INDEX_PATH.is_file():
        raise FileNotFoundError(f"GUI 入口文件不存在：{INDEX_PATH}")
    return INDEX_PATH


def get_icon_path(platform_name: str | None = None) -> Path:
    """根据桌面平台选择对应的窗口图标格式。"""

    platform_name = platform_name or sys.platform
    suffix = {
        "win32": ".ico",
        "darwin": ".icns",
    }.get(platform_name, ".png")
    icon_path = ROOT.joinpath("static", f"XHS-Downloader{suffix}")
    if not icon_path.is_file():
        raise FileNotFoundError(f"GUI 图标文件不存在：{icon_path}")
    return icon_path


def launch() -> None:
    """创建并启动静态 GUI 窗口；窗口关闭后再释放后台下载器。"""

    # 先创建窗口，再异步启动后端，让启动加载层尽早显示。
    backend = GuiBackend()
    index_url = get_index_path().as_uri()
    icon_path = get_icon_path()
    api = GuiApi(backend)
    # 1280x720 为桌面端默认及最小尺寸，前端样式负责更窄窗口的响应式布局。
    window = webview.create_window(
        PROJECT,
        index_url,
        width=1280,
        height=720,
        min_size=(1280, 720),
        resizable=True,
        text_select=True,
        js_api=api,
    )
    api._bind_window(window)
    backend.start(wait=False)
    try:
        webview.start(
            icon=str(icon_path),
        )
    finally:
        backend.stop()


def main() -> None:
    """命令行入口。"""

    launch()


if __name__ == "__main__":
    main()

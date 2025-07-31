from contextlib import suppress
from os import walk
from pathlib import Path


def file_switch(path: Path) -> None:
    if path.exists():
        path.unlink()
    else:
        path.touch()


def remove_empty_directories(path: Path) -> None:
    exclude = {
        "\\.",
        "\\_",
        "\\__",
    }
    # 使用 os.walk 替代 Path.walk 以提高兼容性
    for dir_path, dir_names, file_names in walk(
        str(path),
        topdown=False,
    ):
        dir_path = Path(dir_path)
        if any(i in str(dir_path) for i in exclude):
            continue
        if not dir_names and not file_names:
            with suppress(OSError):
                dir_path.rmdir()

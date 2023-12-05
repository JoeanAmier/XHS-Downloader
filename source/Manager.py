from pathlib import Path
from shutil import move
from shutil import rmtree

__all__ = ["Manager"]


class Manager:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/119.0.0.0 Safari/537.36", }

    def __init__(self, root: Path):
        self.temp = root.joinpath("./temp")

    @staticmethod
    def is_exists(path: Path) -> bool:
        return path.exists()

    @staticmethod
    def delete(path: Path):
        path.unlink()

    @staticmethod
    def move(temp: Path, path: Path):
        move(temp.resolve(), path.resolve())

    def clean(self):
        rmtree(self.temp.resolve())

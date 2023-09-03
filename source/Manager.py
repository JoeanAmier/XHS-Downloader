from pathlib import Path
from shutil import move

__all__ = ['Manager']


class Manager:
    @staticmethod
    def is_exists(path: Path) -> bool:
        return path.exists()

    @staticmethod
    def delete(path: Path):
        path.unlink()

    @staticmethod
    def remove(temp: Path, path: Path):
        move(temp.resolve(), path.resolve())

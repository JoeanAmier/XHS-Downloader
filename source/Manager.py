from pathlib import Path

__all__ = ['Manager']


class Manager:
    @staticmethod
    def is_exists(path: Path) -> bool:
        return path.exists()

    @staticmethod
    def delete(path: Path):
        path.unlink()

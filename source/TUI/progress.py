from textual.app import ComposeResult
from textual.screen import Screen

__all__ = ["Progress"]


class Progress(Screen):
    """Displays download progress in a Textual UI."""

    def compose(self) -> ComposeResult:
        """Compose the progress display widgets."""
        return

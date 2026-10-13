"""Logging setup — rich handler for the CLI, plain file log for the GUI."""

from __future__ import annotations

import logging
from pathlib import Path

from rich.logging import RichHandler

_LOG_DIR = Path.home() / ".d2v-report-studio" / "logs"


def configure_logging(level: int = logging.INFO) -> None:
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(level)

    stream = RichHandler(rich_tracebacks=True, show_path=False)
    stream.setLevel(level)
    root.addHandler(stream)

    file_h = logging.FileHandler(_LOG_DIR / "studio.log", encoding="utf-8")
    file_h.setLevel(logging.DEBUG)
    file_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root.addHandler(file_h)
"""Qt application bootstrap. Wires the main window to the handler registry."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from data_to_video_report_studio.core.engine import ReportEngine
from data_to_video_report_studio.handlers.registry import HandlerRegistry
from data_to_video_report_studio.services.cache_service import RenderCache
from data_to_video_report_studio.services.narration.openai_backend import OpenAINarrationBackend
from data_to_video_report_studio.services.render_service import FfmpegRenderService
from data_to_video_report_studio.ui.main_window import MainWindow
from data_to_video_report_studio.utils.logging import configure_logging


def build_engine() -> ReportEngine:
    cache = RenderCache()
    narration = OpenAINarrationBackend()
    renderer = FfmpegRenderService(cache=cache)
    return ReportEngine(narration=narration, renderer=renderer, cache=cache)


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    app = QApplication(argv if argv is not None else sys.argv)
    engine = build_engine()
    registry = HandlerRegistry(engine=engine)
    window = MainWindow(registry=registry)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
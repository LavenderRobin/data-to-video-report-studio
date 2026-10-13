"""HandlerRegistry — single source of truth for GUI-addressable features."""

from __future__ import annotations

from data_to_video_report_studio.core.engine import ReportEngine
from data_to_video_report_studio.handlers.dataset_handler import DatasetHandler
from data_to_video_report_studio.handlers.export_handler import ExportHandler
from data_to_video_report_studio.handlers.template_handler import TemplateHandler


class HandlerRegistry:
    def __init__(self, engine: ReportEngine) -> None:
        self.engine = engine
        self.dataset = DatasetHandler(engine)
        self.template = TemplateHandler(engine)
        self.export = ExportHandler(engine)

    def all(self) -> dict[str, object]:
        return {"dataset": self.dataset, "template": self.template, "export": self.export}
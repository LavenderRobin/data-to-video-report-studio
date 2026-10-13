"""TemplateHandler — loads a YAML report template and validates sections."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from data_to_video_report_studio.core.engine import ReportEngine
from data_to_video_report_studio.models.template import ReportTemplate
from data_to_video_report_studio.utils.paths import ensure_readable


class TemplateHandler:
    def __init__(self, engine: ReportEngine) -> None:
        self._engine = engine

    def load(self, path: Path) -> ReportTemplate:
        path = ensure_readable(path)
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        try:
            return ReportTemplate.model_validate(raw)
        except ValidationError as exc:
            raise ValueError(f"invalid template {path.name}: {exc}") from exc
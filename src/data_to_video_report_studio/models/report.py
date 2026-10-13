"""ReportResult — final artifact descriptor returned by the engine."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ReportResult:
    video_path: Path
    duration_s: float
    scenes: int

    def summary(self) -> str:
        return f"{self.video_path.name}: {self.scenes} scenes, {self.duration_s:.1f}s"
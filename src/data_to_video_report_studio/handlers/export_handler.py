"""ExportHandler — packages a finished report for sharing."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from data_to_video_report_studio.core.engine import ReportEngine
from data_to_video_report_studio.models.report import ReportResult


@dataclass(slots=True)
class ExportBundle:
    video: Path
    sidecar_srt: Path | None
    manifest: Path


class ExportHandler:
    def __init__(self, engine: ReportEngine) -> None:
        self._engine = engine

    def export(self, result: ReportResult, *, dest_dir: Path) -> ExportBundle:
        dest_dir.mkdir(parents=True, exist_ok=True)
        video_out = dest_dir / result.video_path.name
        shutil.copy2(result.video_path, video_out)
        srt = result.video_path.with_suffix(".srt")
        srt_out = dest_dir / srt.name if srt.exists() else None
        if srt_out is not None:
            shutil.copy2(srt, srt_out)
        manifest = dest_dir / "manifest.txt"
        manifest.write_text(
            f"video={video_out.name}\nduration_s={result.duration_s:.2f}\nscenes={result.scenes}\n",
            encoding="utf-8",
        )
        return ExportBundle(video=video_out, sidecar_srt=srt_out, manifest=manifest)
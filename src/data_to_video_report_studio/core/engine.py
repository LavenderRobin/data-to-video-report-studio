"""ReportEngine — orchestrates dataset -> scenes -> narration -> render."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from data_to_video_report_studio.core.narration_pipeline import NarrationPipeline
from data_to_video_report_studio.core.timeline_builder import TimelineBuilder
from data_to_video_report_studio.models.dataset import Dataset
from data_to_video_report_studio.models.report import ReportResult
from data_to_video_report_studio.models.template import ReportTemplate
from data_to_video_report_studio.services.cache_service import RenderCache
from data_to_video_report_studio.services.narration.base import NarrationBackend
from data_to_video_report_studio.services.render_service import FfmpegRenderService

log = logging.getLogger(__name__)


@dataclass(slots=True)
class ReportEngine:
    narration: NarrationBackend
    renderer: FfmpegRenderService
    cache: RenderCache

    async def build_report(
        self,
        *,
        dataset: Dataset,
        template: ReportTemplate,
        out_path: Path,
        narration: bool = True,
    ) -> ReportResult:
        timeline = TimelineBuilder(template=template).build(dataset)
        log.info("timeline built: %d scenes, %.1fs", len(timeline.scenes), timeline.total_s)

        if narration:
            pipeline = NarrationPipeline(backend=self.narration)
            timeline = await pipeline.attach_narration(timeline, dataset=dataset)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        video_path, duration = await self.renderer.render(timeline, out_path=out_path)
        return ReportResult(video_path=video_path, duration_s=duration, scenes=len(timeline.scenes))
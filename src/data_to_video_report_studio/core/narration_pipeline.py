"""NarrationPipeline — attaches TTS-ready narration text to each scene."""

from __future__ import annotations

import asyncio
import logging

from data_to_video_report_studio.models.dataset import Dataset
from data_to_video_report_studio.models.scene import Scene, SceneKind, Timeline
from data_to_video_report_studio.services.narration.base import NarrationBackend

log = logging.getLogger(__name__)


class NarrationPipeline:
    def __init__(self, backend: NarrationBackend, concurrency: int = 4) -> None:
        self._backend = backend
        self._sem = asyncio.Semaphore(concurrency)

    async def attach_narration(self, timeline: Timeline, *, dataset: Dataset) -> Timeline:
        async def one(scene: Scene) -> Scene:
            if scene.kind is SceneKind.TITLE and not scene.body:
                return scene
            async with self._sem:
                try:
                    text = await self._backend.narrate(scene=scene, dataset=dataset)
                except Exception as exc:  # noqa: BLE001 — narration is best-effort
                    log.warning("narration failed for scene %s: %s", scene.headline, exc)
                    return scene
            return scene.with_narration(text)

        narrated = await asyncio.gather(*(one(s) for s in timeline.scenes))
        return Timeline(scenes=list(narrated))
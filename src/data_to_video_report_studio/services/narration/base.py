"""NarrationBackend protocol — every backend speaks this shape."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from data_to_video_report_studio.models.dataset import Dataset
from data_to_video_report_studio.models.scene import Scene


@runtime_checkable
class NarrationBackend(Protocol):
    name: str

    async def narrate(self, *, scene: Scene, dataset: Dataset) -> str:
        """Return 1-2 sentences of narration text for the given scene."""
        ...
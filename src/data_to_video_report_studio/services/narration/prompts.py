"""Prompt templates for the narration backends."""

from __future__ import annotations

from data_to_video_report_studio.models.dataset import Dataset
from data_to_video_report_studio.models.scene import Scene

_SYSTEM = (
    "You narrate short data-video report scenes. One or two sentences. "
    "No filler. No greetings. Reference the metric by name and its value."
)


def build_prompt(*, scene: Scene, dataset: Dataset) -> str:
    lines = [
        _SYSTEM,
        "",
        f"Dataset: {dataset.name} ({len(dataset.rows)} rows, {len(dataset.columns)} columns)",
        f"Scene kind: {scene.kind.value}",
        f"Headline: {scene.headline}",
    ]
    if scene.body:
        lines.append(f"Body: {scene.body}")
    if scene.chart:
        lines.append(f"Chart: {scene.chart.get('kind')} on column {scene.chart.get('column')}")
    return "\n".join(lines)
"""TimelineBuilder — maps a dataset + template into an ordered scene timeline."""

from __future__ import annotations

from dataclasses import dataclass

from data_to_video_report_studio.models.dataset import Dataset
from data_to_video_report_studio.models.scene import Scene, SceneKind, Timeline
from data_to_video_report_studio.models.template import ReportTemplate

MIN_SCENE_S = 0.5
MAX_SCENE_S = 45.0


@dataclass(slots=True)
class TimelineBuilder:
    template: ReportTemplate

    def build(self, dataset: Dataset) -> Timeline:
        scenes: list[Scene] = []
        scenes.append(self._title_scene(dataset))
        for section in self.template.sections:
            scenes.extend(self._section_scenes(section, dataset))
        scenes.append(self._outro_scene(dataset))
        return Timeline(scenes=scenes)

    def _title_scene(self, dataset: Dataset) -> Scene:
        return Scene(
            kind=SceneKind.TITLE,
            duration_s=2.5,
            headline=self.template.title or dataset.name,
            body=f"{len(dataset.rows)} rows · {len(dataset.columns)} columns",
        )

    def _section_scenes(self, section, dataset: Dataset) -> list[Scene]:
        out: list[Scene] = []
        for metric in section.metrics:
            series = dataset.column(metric.column)
            value = metric.aggregate(series)
            out.append(
                Scene(
                    kind=SceneKind.METRIC,
                    duration_s=_clamp(section.duration_s),
                    headline=metric.label,
                    body=metric.format(value),
                    chart={"kind": metric.chart, "column": metric.column},
                )
            )
        return out

    def _outro_scene(self, dataset: Dataset) -> Scene:
        return Scene(kind=SceneKind.OUTRO, duration_s=2.0, headline="End of report", body=dataset.name)


def _clamp(seconds: float) -> float:
    return max(MIN_SCENE_S, min(MAX_SCENE_S, seconds))
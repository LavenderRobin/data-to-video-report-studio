"""Scene + Timeline schemas."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from enum import Enum
from pathlib import Path
from typing import Any


class SceneKind(str, Enum):
    TITLE = "title"
    METRIC = "metric"
    TABLE = "table"
    CHART = "chart"
    OUTRO = "outro"


@dataclass(slots=True)
class Scene:
    kind: SceneKind
    duration_s: float
    headline: str
    body: str = ""
    chart: dict[str, Any] | None = None
    narration: str | None = None
    filters: list[str] = field(default_factory=list)
    frame_path: Path | None = None

    def with_narration(self, text: str) -> "Scene":
        return replace(self, narration=text)


@dataclass(slots=True)
class Timeline:
    scenes: list[Scene]

    @property
    def total_s(self) -> float:
        return sum(s.duration_s for s in self.scenes)

    def digest(self) -> str:
        blob = json.dumps(
            [{"k": s.kind.value, "h": s.headline, "b": s.body, "d": s.duration_s} for s in self.scenes],
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.blake2b(blob, digest_size=12).hexdigest()
"""DatasetHandler — loads CSV/Parquet/JSON into a validated Dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_to_video_report_studio.core.engine import ReportEngine
from data_to_video_report_studio.models.dataset import Dataset, DatasetSource
from data_to_video_report_studio.utils.paths import ensure_readable


class DatasetHandler:
    def __init__(self, engine: ReportEngine) -> None:
        self._engine = engine

    def load(self, path: Path) -> Dataset:
        path = ensure_readable(path)
        suffix = path.suffix.lower()
        if suffix == ".csv":
            frame = pd.read_csv(path)
            source = DatasetSource.CSV
        elif suffix in {".parquet", ".pq"}:
            frame = pd.read_parquet(path)
            source = DatasetSource.PARQUET
        elif suffix == ".json":
            frame = pd.read_json(path)
            source = DatasetSource.JSON
        else:
            raise ValueError(f"unsupported dataset format: {suffix}")
        return Dataset.from_frame(frame, name=path.stem, source=source)
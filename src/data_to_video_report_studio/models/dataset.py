"""Dataset — validated tabular data wrapper around a pandas DataFrame."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

import pandas as pd


class DatasetSource(str, Enum):
    CSV = "csv"
    PARQUET = "parquet"
    JSON = "json"


@dataclass(slots=True)
class Dataset:
    name: str
    source: DatasetSource
    columns: list[str]
    rows: list[dict[str, Any]]

    @classmethod
    def from_frame(cls, frame: pd.DataFrame, *, name: str, source: DatasetSource) -> "Dataset":
        frame = frame.dropna(how="all")
        return cls(
            name=name,
            source=source,
            columns=[str(c) for c in frame.columns],
            rows=frame.to_dict(orient="records"),
        )

    def column(self, name: str) -> pd.Series:
        if name not in self.columns:
            raise KeyError(f"column not in dataset: {name}")
        return pd.Series([row.get(name) for row in self.rows])

    def head(self, n: int = 5) -> list[dict[str, Any]]:
        return self.rows[:n]
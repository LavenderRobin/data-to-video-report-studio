"""ReportTemplate — YAML-driven description of a report's sections."""

from __future__ import annotations

from typing import Any, Callable, Literal

import pandas as pd
from pydantic import BaseModel, Field

Aggregate = Literal["sum", "mean", "min", "max", "count", "last"]


class MetricSpec(BaseModel):
    label: str
    column: str
    aggregate: Aggregate = "sum"
    chart: Literal["line", "bar", "pie", "none"] = "bar"
    fmt: str = "{:,.2f}"

    def aggregate_value(self, series: pd.Series) -> float:
        return float(getattr(series, self.aggregate)())

    def format(self, value: float) -> str:
        try:
            return self.fmt.format(value)
        except (ValueError, KeyError):
            return str(value)


class SectionSpec(BaseModel):
    name: str
    duration_s: float = Field(default=4.0, ge=0.5, le=45.0)
    metrics: list[MetricSpec]


class ReportTemplate(BaseModel):
    title: str = ""
    sections: list[SectionSpec]
    theme: dict[str, Any] = Field(default_factory=dict)

    def metric_columns(self) -> list[str]:
        return [m.column for s in self.sections for m in s.metrics]
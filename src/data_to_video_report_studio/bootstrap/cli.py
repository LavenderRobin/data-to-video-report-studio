"""Headless CLI: `d2v-render --dataset data.csv --template weekly.yaml`."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from rich.console import Console

from data_to_video_report_studio.bootstrap.app import build_engine
from data_to_video_report_studio.handlers.dataset_handler import DatasetHandler
from data_to_video_report_studio.handlers.template_handler import TemplateHandler
from data_to_video_report_studio.utils.logging import configure_logging

console = Console()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="d2v-render")
    p.add_argument("--dataset", type=Path, required=True)
    p.add_argument("--template", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("renders/report.mp4"))
    p.add_argument("--no-narration", action="store_true")
    return p.parse_args()


async def _run(args: argparse.Namespace) -> int:
    engine = build_engine()
    dataset = DatasetHandler(engine).load(args.dataset)
    template = TemplateHandler(engine).load(args.template)
    result = await engine.build_report(
        dataset=dataset,
        template=template,
        out_path=args.out,
        narration=not args.no_narration,
    )
    console.print(f"[green]rendered[/green] {result.video_path} ({result.duration_s:.1f}s)")
    return 0


def main() -> int:
    configure_logging()
    return asyncio.run(_run(parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
"""FfmpegRenderService — composes scene frames + audio into a final MP4."""

from __future__ import annotations

import asyncio
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path

from data_to_video_report_studio.models.scene import Timeline
from data_to_video_report_studio.services.cache_service import RenderCache

log = logging.getLogger(__name__)

_ALLOWED_FILTERS = {"fade", "scale", "pad", "overlay", "drawtext", "concat", "format", "trim"}


@dataclass(slots=True)
class FfmpegRenderService:
    cache: RenderCache
    ffmpeg_bin: str = "ffmpeg"

    async def render(self, timeline: Timeline, *, out_path: Path) -> tuple[Path, float]:
        self._validate_filters(timeline)
        binary = self._resolve_ffmpeg()
        args = self._build_args(timeline, out_path=out_path)
        log.info("ffmpeg render: %d scenes -> %s", len(timeline.scenes), out_path)
        proc = await asyncio.create_subprocess_exec(
            binary, *args, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"ffmpeg failed ({proc.returncode}): {stderr.decode(errors='replace')[-800:]}")
        return out_path, timeline.total_s

    def _resolve_ffmpeg(self) -> str:
        if shutil.which(self.ffmpeg_bin):
            return self.ffmpeg_bin
        try:
            import imageio_ffmpeg  # type: ignore[import-not-found]

            return imageio_ffmpeg.get_ffmpeg_exe()
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("ffmpeg not found; install imageio-ffmpeg or add ffmpeg.exe to PATH") from exc

    def _validate_filters(self, timeline: Timeline) -> None:
        for scene in timeline.scenes:
            for f in scene.filters:
                name = f.split("=", 1)[0]
                if name not in _ALLOWED_FILTERS:
                    raise ValueError(f"filter not allowed: {name}")

    def _build_args(self, timeline: Timeline, *, out_path: Path) -> list[str]:
        # Concatenate per-scene frames produced by the chart renderer.
        concat_manifest = self.cache.path_for(timeline.digest(), ext="txt")
        concat_manifest.write_text(
            "\n".join(f"file '{s.frame_path.as_posix()}'" for s in timeline.scenes if s.frame_path),
            encoding="utf-8",
        )
        return [
            "-y", "-f", "concat", "-safe", "0", "-i", str(concat_manifest),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium",
            str(out_path),
        ]
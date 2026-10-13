"""Path helpers for dataset/template loading."""

from __future__ import annotations

from pathlib import Path

_MAX_BYTES = 512 * 1024 * 1024  # 512 MB — refuse to load anything bigger into memory


def ensure_readable(path: Path) -> Path:
    path = path.expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(path)
    if not path.is_file():
        raise IsADirectoryError(path)
    if path.stat().st_size > _MAX_BYTES:
        raise ValueError(f"file too large to load: {path.stat().st_size} bytes")
    return path
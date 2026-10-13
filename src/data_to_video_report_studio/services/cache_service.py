"""RenderCache — content-addressed cache for scene frames and TTS clips."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RenderCache:
    root: Path = Path.home() / ".d2v-report-studio" / "cache"

    def key_for(self, payload: dict) -> str:
        blob = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
        return hashlib.blake2b(blob, digest_size=16).hexdigest()

    def path_for(self, key: str, *, ext: str) -> Path:
        shard = key[:2]
        p = self.root / shard / f"{key}.{ext}"
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def has(self, key: str, *, ext: str) -> bool:
        return self.path_for(key, ext=ext).exists()
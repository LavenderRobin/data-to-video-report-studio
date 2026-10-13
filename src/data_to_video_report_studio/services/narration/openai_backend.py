"""OpenAI narration backend. Reads OPENAI_API_KEY from env or keyring."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from openai import AsyncOpenAI

from data_to_video_report_studio.models.dataset import Dataset
from data_to_video_report_studio.models.scene import Scene
from data_to_video_report_studio.services.narration.prompts import build_prompt


@dataclass(slots=True)
class OpenAINarrationBackend:
    model: str = "gpt-4o-mini"
    name: str = "openai"
    _client: AsyncOpenAI = field(init=False, repr=False)

    def __post_init__(self) -> None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            try:
                import keyring  # type: ignore[import-not-found]

                api_key = keyring.get_password("d2v-report-studio", "openai")
            except Exception:  # noqa: BLE001
                api_key = None
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set and no keyring entry found")
        self._client = AsyncOpenAI(api_key=api_key)

    async def narrate(self, *, scene: Scene, dataset: Dataset) -> str:
        prompt = build_prompt(scene=scene, dataset=dataset)
        resp = await self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You write tight, factual video-report narration."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=120,
        )
        return (resp.choices[0].message.content or "").strip()
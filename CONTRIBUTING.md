# Contributing to data-to-video-report-studio

Thanks for wanting to push pixels and pull rows. This repo turns tabular
datasets into narrated video reports using a local render pipeline plus an
optional LLM narration backend.

## Dev setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,render]"
d2v-studio --debug
```

FFmpeg: install `imageio-ffmpeg` (bundled binary) or drop a static
`ffmpeg.exe` on `PATH`. The renderer probes both and logs which one it used
(`services/render_service.py`).

## Layout

- `bootstrap/` — entry points (`app.py` GUI, `cli.py` headless)
- `core/` — engine: timeline builder, narration pipeline, render scheduler
- `handlers/` — feature handlers wired to the GUI (dataset, template, export)
- `services/` — long-lived services (LLM narration, ffmpeg render, cache)
- `models/` — pydantic schemas for datasets, scenes, reports
- `utils/` — logging, timing, path helpers
- `config/` — YAML defaults and prompt templates

## Rules

1. Every handler is registered in `handlers/registry.py`. No orphan handlers.
2. No blocking calls on the Qt main thread. Use `core/task_runner.py`.
3. New narration backends go in `services/narration/` and must implement
   `NarrationBackend` from `services/narration/base.py`.
4. Tests: `pytest -q`. GPU/ffmpeg tests are marked `@pytest.mark.render`.

## Commit style

`<area>: <imperative summary>` — e.g. `timeline: clamp scene duration to 0.5s min`.
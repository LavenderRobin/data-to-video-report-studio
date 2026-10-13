# Security Policy

## Reporting

Email `security@d2v-report-studio.dev` with steps to reproduce. We aim to
ack ack within 72h and ship a patch within 14 days for confirmed issues.

## Scope

- Local desktop app. No server component ships in this repo.
- Narration backends that call remote APIs (OpenAI, Azure, local Ollama)
  handle user API keys. Keys are read from environment variables or the
  Windows Credential Manager via `keyring`; they are never written to
  project files or logs.
- Rendered videos may embed dataset contents. Treat `renders/` as
  sensitive when datasets are confidential.

## Threat model

- Malicious dataset files (CSV/Parquet) — parsed with pandas; no `eval`.
- Malicious Jinja2 templates — rendered with `SandboxedEnvironment`
  (`services/template_service.py`).
- Malicious ffmpeg filters — filter strings are validated against an
  allowlist in `services/render_service.py` before subprocess launch.
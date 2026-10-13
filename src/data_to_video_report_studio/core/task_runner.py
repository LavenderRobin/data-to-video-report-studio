"""TaskRunner — runs async engine work off the Qt main thread."""

from __future__ import annotations

import asyncio
from collections.abc import Coroutine
from typing import Any

from PySide6.QtCore import QObject, QThread, Signal


class _Worker(QThread):
    done = Signal(object)
    failed = Signal(Exception)

    def __init__(self, coro: Coroutine[Any, Any, Any]) -> None:
        super().__init__()
        self._coro = coro

    def run(self) -> None:  # noqa: D401 — QThread entry
        try:
            result = asyncio.run(self._coro)
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(exc)
            return
        self.done.emit(result)


class TaskRunner(QObject):
    """Owns the worker threads so they don't get GC'd mid-flight."""

    def __init__(self) -> None:
        super().__init__()
        self._active: list[_Worker] = []

    def submit(self, coro: Coroutine[Any, Any, Any], *, on_done, on_fail) -> None:
        worker = _Worker(coro)
        worker.done.connect(on_done)
        worker.failed.connect(on_fail)
        worker.finished.connect(lambda: self._active.remove(worker) if worker in self._active else None)
        self._active.append(worker)
        worker.start()
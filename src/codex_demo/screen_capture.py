"""Screen capture abstraction for the demo pipeline."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterator, Tuple

from codex_demo.models import Frame


@dataclass
class CaptureConfig:
    fps: int = 15
    region: Tuple[int, int, int, int] | None = None


class ScreenCapture:
    """Produces Frame objects at a fixed frame rate.

    Replace this with a real screen capture backend (mss, dxcam, etc.) when
    integrating with an actual environment.
    """

    def __init__(self, config: CaptureConfig) -> None:
        self._config = config
        self._running = False

    def frames(self) -> Iterator[Frame]:
        self._running = True
        interval = 1.0 / max(self._config.fps, 1)
        frame_index = 0
        while self._running:
            now = time.time()
            yield Frame(index=frame_index, timestamp=now)
            frame_index += 1
            time.sleep(interval)

    def stop(self) -> None:
        self._running = False

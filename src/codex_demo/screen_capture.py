"""Screen capture abstraction for the demo pipeline."""

from __future__ import annotations

import time
from dataclasses import dataclass
from importlib.util import find_spec
from typing import Iterator, Tuple

from codex_demo.models import Frame


@dataclass
class CaptureConfig:
    fps: int = 15
    region: Tuple[int, int, int, int] | None = None


class ScreenCapture:
    """Produces Frame objects at a fixed frame rate.

    Uses `mss` to capture a region of the screen and returns frames as NumPy
    arrays (BGR). Requires `mss` + `numpy` + `opencv-python`.
    """

    def __init__(self, config: CaptureConfig) -> None:
        self._config = config
        self._running = False

    def frames(self) -> Iterator[Frame]:
        self._ensure_dependencies()
        import cv2
        import numpy as np
        from mss import mss

        self._running = True
        interval = 1.0 / max(self._config.fps, 1)
        frame_index = 0
        with mss() as sct:
            monitor = self._monitor_from_region(sct)
            while self._running:
                now = time.time()
                raw = sct.grab(monitor)
                frame_bgra = np.array(raw)
                frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
                yield Frame(
                    index=frame_index,
                    timestamp=now,
                    image=frame_bgr,
                    region=self._config.region,
                )
                frame_index += 1
                time.sleep(interval)

    def stop(self) -> None:
        self._running = False

    def _monitor_from_region(self, sct) -> dict:
        if self._config.region is None:
            return sct.monitors[1]
        left, top, width, height = self._config.region
        return {"left": left, "top": top, "width": width, "height": height}

    @staticmethod
    def _ensure_dependencies() -> None:
        missing = [
            name
            for name in ("mss", "numpy", "cv2")
            if find_spec(name) is None
        ]
        if missing:
            missing_list = ", ".join(missing)
            raise RuntimeError(
                f"Missing dependencies for screen capture: {missing_list}. "
                "Install requirements.txt to proceed."
            )

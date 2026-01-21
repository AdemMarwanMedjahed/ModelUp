"""Object detection for the demo pipeline (simple color-based detector)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple

from importlib.util import find_spec

from codex_demo.models import Detection, Frame


@dataclass
class DetectorConfig:
    label: str = "resource"
    hsv_lower: Tuple[int, int, int] = (25, 80, 80)
    hsv_upper: Tuple[int, int, int] = (40, 255, 255)
    min_area: int = 150
    max_detections: int = 5


class Detector:
    """Detects targets by HSV color thresholding."""

    def __init__(self, config: DetectorConfig) -> None:
        self._config = config

    def detect(self, frame: Frame) -> List[Detection]:
        self._ensure_dependencies()
        import cv2
        import numpy as np

        image = frame.image
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array(self._config.hsv_lower)
        upper = np.array(self._config.hsv_upper)
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections: List[Detection] = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self._config.min_area:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            center = (x + w // 2, y + h // 2)
            confidence = min(area / 2000.0, 1.0)
            detections.append(
                Detection(label=self._config.label, confidence=confidence, position=center)
            )
        detections.sort(key=lambda det: det.confidence, reverse=True)
        detections = detections[: self._config.max_detections]
        return detections

    @staticmethod
    def best_target(detections: Iterable[Detection]) -> Detection | None:
        return max(detections, key=lambda det: det.confidence, default=None)

    @staticmethod
    def _ensure_dependencies() -> None:
        missing = [name for name in ("cv2", "numpy") if find_spec(name) is None]
        if missing:
            missing_list = ", ".join(missing)
            raise RuntimeError(
                f"Missing dependencies for detection: {missing_list}. "
                "Install requirements.txt to proceed."
            )

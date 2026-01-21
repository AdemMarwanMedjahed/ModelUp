"""Object detection stub for the demo pipeline."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, List, Tuple

from codex_demo.models import Detection, Frame


@dataclass
class DetectorConfig:
    labels: Tuple[str, ...] = ("resource_a", "resource_b", "resource_c")
    max_detections: int = 3
    min_confidence: float = 0.5


class Detector:
    """Produces synthetic detections.

    Swap this with a real detector (YOLO, template matching, color+contours) to
    hook into the actual computer-vision pipeline.
    """

    def __init__(self, config: DetectorConfig) -> None:
        self._config = config

    def detect(self, frame: Frame) -> List[Detection]:
        random.seed(frame.index)
        detections: List[Detection] = []
        for _ in range(random.randint(0, self._config.max_detections)):
            label = random.choice(self._config.labels)
            confidence = random.uniform(self._config.min_confidence, 0.95)
            position = (random.randint(0, 1920), random.randint(0, 1080))
            detections.append(Detection(label=label, confidence=confidence, position=position))
        return detections

    @staticmethod
    def best_target(detections: Iterable[Detection]) -> Detection | None:
        return max(detections, key=lambda det: det.confidence, default=None)

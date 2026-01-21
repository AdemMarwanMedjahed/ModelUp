"""Entry point for running the demo pipeline."""

from __future__ import annotations

import itertools
import logging

from codex_demo.action_executor import ActionConfig, ActionExecutor
from codex_demo.decision_engine import DecisionEngine
from codex_demo.detector import Detector, DetectorConfig
from codex_demo.screen_capture import CaptureConfig, ScreenCapture


def run(max_cycles: int = 25) -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger("codex_demo")

    capture = ScreenCapture(CaptureConfig(fps=10, region=None))
    detector = Detector(DetectorConfig())
    decision_engine = DecisionEngine()
    executor = ActionExecutor(ActionConfig(), logger.info)

    for frame in itertools.islice(capture.frames(), max_cycles):
        detections = detector.detect(frame)
        decision = decision_engine.decide(detections)
        logger.info(
            "[Frame %s] state=%s detections=%s", frame.index, decision_engine.context.state, len(detections)
        )
        executor.execute(decision.action, decision.target)

    capture.stop()


if __name__ == "__main__":
    run()

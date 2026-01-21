"""Entry point for running the demo pipeline."""

from __future__ import annotations

import argparse
import itertools
import logging

from codex_demo.action_executor import ActionConfig, ActionExecutor
from codex_demo.decision_engine import DecisionEngine
from codex_demo.detector import Detector, DetectorConfig
from codex_demo.screen_capture import CaptureConfig, ScreenCapture


def run(args: argparse.Namespace) -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger("codex_demo")

    capture = ScreenCapture(CaptureConfig(fps=args.fps, region=args.roi))
    detector = Detector(
        DetectorConfig(
            label=args.label,
            hsv_lower=tuple(args.hsv_lower),
            hsv_upper=tuple(args.hsv_upper),
            min_area=args.min_area,
            max_detections=args.max_detections,
        )
    )
    decision_engine = DecisionEngine()
    executor = ActionExecutor(
        ActionConfig(base_delay_s=args.base_delay, jitter_s=args.jitter, dry_run=args.dry_run),
        logger.info,
    )

    for frame in itertools.islice(capture.frames(), args.max_cycles):
        detections = detector.detect(frame)
        decision = decision_engine.decide(detections)
        logger.info(
            "[Frame %s] state=%s detections=%s", frame.index, decision_engine.context.state, len(detections)
        )
        executor.execute(decision.action, decision.target)

    capture.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Codex demo pipeline.")
    parser.add_argument("--fps", type=int, default=10, help="Frames per second for capture.")
    parser.add_argument("--max-cycles", type=int, default=200, help="Maximum frames to process.")
    parser.add_argument("--label", default="resource", help="Label for detections.")
    parser.add_argument(
        "--hsv-lower",
        type=int,
        nargs=3,
        default=(25, 80, 80),
        help="Lower HSV bound for color detection.",
    )
    parser.add_argument(
        "--hsv-upper",
        type=int,
        nargs=3,
        default=(40, 255, 255),
        help="Upper HSV bound for color detection.",
    )
    parser.add_argument("--min-area", type=int, default=150, help="Minimum contour area.")
    parser.add_argument("--max-detections", type=int, default=5, help="Maximum detections per frame.")
    parser.add_argument(
        "--roi",
        type=int,
        nargs=4,
        metavar=("LEFT", "TOP", "WIDTH", "HEIGHT"),
        help="Capture region of interest.",
    )
    parser.add_argument("--base-delay", type=float, default=0.15, help="Base action delay in seconds.")
    parser.add_argument("--jitter", type=float, default=0.1, help="Action delay jitter in seconds.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Log actions without clicking (recommended for safety).",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Enable real mouse actions via pynput (disables dry-run).",
    )
    parsed = parser.parse_args()
    if parsed.live:
        parsed.dry_run = False
    run(parsed)

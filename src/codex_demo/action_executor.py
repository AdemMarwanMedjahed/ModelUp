"""Action executor stub for the demo pipeline."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable

from codex_demo.models import Detection


@dataclass
class ActionConfig:
    base_delay_s: float = 0.15
    jitter_s: float = 0.1


class ActionExecutor:
    """Simulates high-level actions with logging hooks."""

    def __init__(self, config: ActionConfig, logger: Callable[[str], None]) -> None:
        self._config = config
        self._logger = logger

    def execute(self, action: str, target: Detection | None) -> None:
        if action == "scan":
            self._logger("[Action] Scanning for targets")
        elif action == "move_to_target" and target:
            self._logger(f"[Action] Moving to {target.label} at {target.position}")
        elif action == "interact" and target:
            self._logger(f"[Action] Harvesting {target.label} at {target.position}")
        elif action == "mount":
            self._logger("[Action] Mounting")
        elif action == "return_search":
            self._logger("[Action] Returning to search")
        else:
            self._logger(f"[Action] No-op for action={action}")

        delay = self._config.base_delay_s + random.random() * self._config.jitter_s
        time.sleep(delay)

"""Action executor stub for the demo pipeline."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from importlib.util import find_spec
from typing import Callable

from codex_demo.models import Detection


@dataclass
class ActionConfig:
    base_delay_s: float = 0.15
    jitter_s: float = 0.1
    dry_run: bool = True


class ActionExecutor:
    """Executes high-level actions with optional mouse control."""

    def __init__(self, config: ActionConfig, logger: Callable[[str], None]) -> None:
        self._config = config
        self._logger = logger
        self._mouse = self._init_mouse()

    def execute(self, action: str, target: Detection | None) -> None:
        if action == "scan":
            self._logger("[Action] Scanning for targets")
        elif action == "move_to_target" and target:
            self._logger(f"[Action] Moving to {target.label} at {target.position}")
        elif action == "interact" and target:
            self._logger(f"[Action] Harvesting {target.label} at {target.position}")
            self._click(target.position)
        elif action == "mount":
            self._logger("[Action] Mounting")
        elif action == "return_search":
            self._logger("[Action] Returning to search")
        else:
            self._logger(f"[Action] No-op for action={action}")

        delay = self._config.base_delay_s + random.random() * self._config.jitter_s
        time.sleep(delay)

    def _init_mouse(self):
        if self._config.dry_run:
            return None
        if find_spec("pynput") is None:
            raise RuntimeError("Missing dependency 'pynput' for real actions.")
        from pynput.mouse import Button, Controller

        return Controller(), Button

    def _click(self, position: tuple[int, int]) -> None:
        if self._config.dry_run or self._mouse is None:
            return
        controller, button = self._mouse
        controller.position = position
        controller.click(button.left, 1)

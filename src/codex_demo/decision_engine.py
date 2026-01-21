"""Decision engine implementing the state machine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from codex_demo.models import DecisionContext, Detection, State


@dataclass
class Decision:
    action: str
    target: Detection | None
    next_state: State


class DecisionEngine:
    """Simple state machine for resource harvesting."""

    def __init__(self) -> None:
        self._context = DecisionContext()

    @property
    def context(self) -> DecisionContext:
        return self._context

    def decide(self, detections: Iterable[Detection]) -> Decision:
        target = self._select_target(detections)
        state = self._context.state

        if state == State.SEARCH:
            if target:
                return self._transition("move_to_target", target, State.MOVE_TO_TARGET)
            return self._transition("scan", None, State.SEARCH)

        if state == State.MOVE_TO_TARGET:
            if target:
                return self._transition("interact", target, State.HARVEST)
            return self._transition("return_search", None, State.RETURN_SEARCH)

        if state == State.HARVEST:
            return self._transition("mount", None, State.MOUNT)

        if state == State.MOUNT:
            return self._transition("return_search", None, State.RETURN_SEARCH)

        if state == State.RETURN_SEARCH:
            return self._transition("scan", None, State.SEARCH)

        return self._transition("scan", None, State.SEARCH)

    def _select_target(self, detections: Iterable[Detection]) -> Optional[Detection]:
        best = max(detections, key=lambda det: det.confidence, default=None)
        if best:
            self._context.last_target = best
            self._context.cycles_without_target = 0
            return best
        self._context.cycles_without_target += 1
        return None

    def _transition(self, action: str, target: Detection | None, next_state: State) -> Decision:
        self._context.state = next_state
        return Decision(action=action, target=target, next_state=next_state)

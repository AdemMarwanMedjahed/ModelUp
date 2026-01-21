"""Shared data structures for the demo pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Tuple


class State(str, Enum):
    SEARCH = "SEARCH"
    MOVE_TO_TARGET = "MOVE_TO_TARGET"
    HARVEST = "HARVEST"
    MOUNT = "MOUNT"
    RETURN_SEARCH = "RETURN_SEARCH"


@dataclass(frozen=True)
class Detection:
    label: str
    confidence: float
    position: Tuple[int, int]


@dataclass
class DecisionContext:
    state: State = State.SEARCH
    last_target: Detection | None = None
    cycles_without_target: int = 0


@dataclass
class Frame:
    """Represents a captured frame."""

    index: int
    timestamp: float
    image: Any
    region: Tuple[int, int, int, int] | None = None

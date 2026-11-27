"""Motion-gating state machine to freeze updates while hands or cards are moving."""

from __future__ import annotations

from typing import Any

import numpy as np

from src.models import MotionState


class MotionGate:
    """Tracks frame-to-frame motion energy and requires consecutive calm frames."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def update(self, warped_bgr: np.ndarray) -> MotionState:
        """Update motion state from the latest canonical table frame."""
        raise NotImplementedError("TODO: Milestone M4")

    def reset(self) -> None:
        """Reset previous-frame reference and stability counters."""
        raise NotImplementedError("TODO: Milestone M4")

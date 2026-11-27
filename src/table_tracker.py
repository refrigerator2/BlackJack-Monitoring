"""Temporal card tracker, stable-frame memory, and Split detection."""

from __future__ import annotations

from typing import Any

import numpy as np

from src.models import CardDetection, MotionState, TableState, ZoneConfig


class TableTracker:
    """Maintains persistent card IDs and hand states across video frames."""

    def __init__(self, zones: list[ZoneConfig], config: dict[str, Any]) -> None:
        self.zones = zones
        self.config = config

    def update(
        self,
        frame_idx: int,
        timestamp_sec: float,
        motion_state: MotionState,
        detections: list[CardDetection],
        warped_bgr: np.ndarray | None = None,
    ) -> TableState:
        """Update tracked hands and emit ADD/MOVE/REMOVE/FLIP/SPLIT events."""
        raise NotImplementedError("TODO: Milestone M4")

    def reset_round(self) -> None:
        """Clear all active hands and card tracks for a new round."""
        raise NotImplementedError("TODO: Milestone M4")

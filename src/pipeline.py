"""End-to-end frame processing pipeline tying all classical CV stages together."""

from __future__ import annotations

from typing import Any

import numpy as np

from src.models import TableCalibration, TableState


class BlackjackPipeline:
    """Coordinates calibration warp, motion gating, detection, tracking, and HUD."""

    def __init__(self, config: dict[str, Any], calibration: TableCalibration) -> None:
        self.config = config
        self.calibration = calibration

    def process_frame(
        self,
        frame_bgr: np.ndarray,
        frame_idx: int,
        timestamp_sec: float,
    ) -> tuple[TableState, np.ndarray]:
        """Process a single raw BGR frame and return (TableState, annotated_bgr)."""
        raise NotImplementedError("TODO: Milestone M4")

    def recalibrate_background(self, frame_bgr: np.ndarray) -> None:
        """Re-sample green-felt background statistics from a live empty table frame."""
        raise NotImplementedError("TODO: Milestone M6")

    def reset_round(self) -> None:
        """Reset tracker state for a new round."""
        raise NotImplementedError("TODO: Milestone M4")

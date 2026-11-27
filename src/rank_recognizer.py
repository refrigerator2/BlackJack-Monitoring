"""13-rank template matching (NCC) and classical disambiguation rules."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np


class RankRecognizer:
    """Matches oriented corner-index patches against calibrated 13-rank templates."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def load_templates(self, templates_dir: str | Path) -> None:
        """Load calibrated grayscale rank templates (A, 2..10, J, Q, K)."""
        raise NotImplementedError("TODO: Milestone M2")

    def recognize_corner(self, corner_patch_bgr: np.ndarray) -> tuple[str | None, float]:
        """Return (best_rank, ncc_score) for a rectified corner-index crop."""
        raise NotImplementedError("TODO: Milestone M2")

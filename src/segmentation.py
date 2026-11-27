"""Green-felt background subtraction and morphological foreground segmentation."""

from __future__ import annotations

from typing import Any

import numpy as np

from src.models import ZoneConfig


class TableSegmenter:
    """Segments playing cards from the uniform green table surface."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def calibrate_background(self, empty_warped_bgr: np.ndarray) -> None:
        """Estimate green-felt BGR/HSV statistics from an empty table frame."""
        raise NotImplementedError("TODO: Milestone M1")

    def segment_foreground(self, warped_bgr: np.ndarray) -> np.ndarray:
        """Return a binary uint8 mask (0/255) of non-background foreground objects."""
        raise NotImplementedError("TODO: Milestone M1")

    def extract_zone_mask(self, fg_mask: np.ndarray, zone: ZoneConfig) -> np.ndarray:
        """Crop or mask the global foreground mask to a specific table zone."""
        raise NotImplementedError("TODO: Milestone M1")

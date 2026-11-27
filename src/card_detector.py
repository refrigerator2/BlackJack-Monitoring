"""Card localization (isolated & shingled stacks) and face-down classification."""

from __future__ import annotations

from typing import Any

import numpy as np

from src.models import CardDetection, ZoneConfig


class CardDetector:
    """Detects isolated and overlapping cards within a zone mask."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def detect_in_zone(
        self,
        warped_bgr: np.ndarray,
        zone_mask: np.ndarray,
        zone: ZoneConfig,
    ) -> list[CardDetection]:
        """Locate cards and visible corner indices inside a single table zone."""
        raise NotImplementedError("TODO: Milestone M2")

    def is_face_down(self, card_patch_bgr: np.ndarray) -> bool:
        """Classify whether a localized card patch is face-down using border/interior stats."""
        raise NotImplementedError("TODO: Milestone M3")

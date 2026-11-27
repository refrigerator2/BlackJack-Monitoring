"""Real-time OpenCV HUD overlay for zones, cards, scores, Split badges, and FPS."""

from __future__ import annotations

from typing import Any

import numpy as np

from src.models import TableState, ZoneConfig


class HUDRenderer:
    """Draws table state overlays onto the canonical warped BGR frame."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def render(
        self,
        warped_bgr: np.ndarray,
        state: TableState,
        zones: list[ZoneConfig],
        debug_mask: np.ndarray | None = None,
    ) -> np.ndarray:
        """Return an annotated BGR frame ready for display or video export."""
        raise NotImplementedError("TODO: Milestone M6")

"""4-point table homography calibration and rectangular zone utilities."""

from __future__ import annotations

import numpy as np

from src.models import CANONICAL_CANVAS_SIZE, TableCalibration, ZoneConfig


def compute_homography(
    src_corners: list[tuple[float, float]],
    canvas_size: tuple[int, int] = CANONICAL_CANVAS_SIZE,
) -> np.ndarray:
    """Compute a 3x3 perspective homography mapping src_corners to the canonical canvas."""
    raise NotImplementedError("TODO: Milestone M1")


def warp_table(frame_bgr: np.ndarray, calibration: TableCalibration) -> np.ndarray:
    """Warp a raw BGR frame into the canonical top-down table canvas."""
    raise NotImplementedError("TODO: Milestone M1")


def build_default_zones(
    canvas_width: int = CANONICAL_CANVAS_SIZE[0],
    canvas_height: int = CANONICAL_CANVAS_SIZE[1],
    num_players: int = 3,
) -> list[ZoneConfig]:
    """Generate default rectangular zones (DEALER top row, P1..PN bottom row)."""
    raise NotImplementedError("TODO: Milestone M1")

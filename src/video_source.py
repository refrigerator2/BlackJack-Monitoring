"""Unified video capture interface for .mp4 files and live DroidCam streams."""

from __future__ import annotations

from typing import Any

import numpy as np


class VideoSource:
    """Wrapper around cv2.VideoCapture for recorded videos and live camera feeds."""

    def __init__(self, source: str | int, target_fps: int | None = None) -> None:
        self.source = source
        self.target_fps = target_fps

    def __enter__(self) -> VideoSource:
        raise NotImplementedError("TODO: Milestone M1")

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.release()

    def read(self) -> tuple[bool, np.ndarray | None]:
        """Read the next BGR frame from the video source."""
        raise NotImplementedError("TODO: Milestone M1")

    @property
    def fps(self) -> float:
        """Return nominal frames per second of the stream."""
        raise NotImplementedError("TODO: Milestone M1")

    @property
    def frame_size(self) -> tuple[int, int]:
        """Return (width, height) of the raw input frames."""
        raise NotImplementedError("TODO: Milestone M1")

    def release(self) -> None:
        """Release underlying capture resources."""
        return None

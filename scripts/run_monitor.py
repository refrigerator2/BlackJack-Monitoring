"""Main CLI entry point for offline video analysis and live DroidCam monitoring."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run Blackjack table monitoring pipeline.")
    src_group = parser.add_mutually_exclusive_group(required=True)
    src_group.add_argument("--video", help="Path to pre-recorded .mp4 gameplay video.")
    src_group.add_argument("--camera", help="Camera index (e.g. 0) or DroidCam HTTP/RTSP URL.")
    parser.add_argument("--config", default="configs/default_config.yaml", help="YAML config path.")
    parser.add_argument("--calibration", default="configs/calibration.json", help="Calibration JSON path.")
    parser.add_argument("--save", action="store_true", help="Save annotated output video.")
    return parser.parse_args()


def main() -> None:
    """Entry point for Blackjack table monitoring."""
    _ = parse_args()
    raise NotImplementedError("TODO: Milestone M4")


if __name__ == "__main__":
    main()

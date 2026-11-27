"""CLI tool for 4-point table homography calibration and zone setup."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Calibrate Blackjack table homography and zones.")
    parser.add_argument("--source", required=True, help="Video path, image path, or camera URL/index.")
    parser.add_argument("--output", default="configs/calibration.json", help="Output calibration JSON path.")
    parser.add_argument("--players", type=int, default=3, help="Number of player zones (minimum 3).")
    return parser.parse_args()


def main() -> None:
    """Entry point for table calibration."""
    _ = parse_args()
    raise NotImplementedError("TODO: Milestone M1")


if __name__ == "__main__":
    main()

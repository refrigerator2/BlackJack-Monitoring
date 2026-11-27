"""CLI tool to extract and normalize the 13 calibrated rank templates."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Capture 13-rank templates from a reference photo.")
    parser.add_argument("--image", required=True, help="Path to reference image containing deck cards.")
    parser.add_argument("--output", default="assets/templates", help="Directory to save rank templates.")
    return parser.parse_args()


def main() -> None:
    """Entry point for template capture."""
    _ = parse_args()
    raise NotImplementedError("TODO: Milestone M2")


if __name__ == "__main__":
    main()

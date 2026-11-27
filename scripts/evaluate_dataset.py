"""CLI tool to benchmark accuracy and FPS against annotated test videos."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Evaluate pipeline on annotated Blackjack videos.")
    parser.add_argument("--dataset-dir", required=True, help="Directory with test videos and JSON labels.")
    parser.add_argument("--config", default="configs/default_config.yaml", help="YAML config path.")
    return parser.parse_args()


def main() -> None:
    """Entry point for dataset evaluation."""
    _ = parse_args()
    raise NotImplementedError("TODO: Milestone M6")


if __name__ == "__main__":
    main()

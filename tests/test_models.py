"""Smoke tests for shared data contracts, config loading, and module imports."""

from __future__ import annotations

import importlib
import tempfile
import unittest
from pathlib import Path

from src.models import (
    CANONICAL_CANVAS_SIZE,
    VALID_RANKS,
    CardDetection,
    CardStatus,
    HandState,
    HandStatus,
    MotionState,
    TableCalibration,
    TableEvent,
    TableEventType,
    TableState,
    TrackedCard,
    ZoneConfig,
    load_config,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestM0Scaffold(unittest.TestCase):
    """Verify M0 package structure, config loading, and data contract serialization."""

    def test_all_src_modules_import_cleanly(self) -> None:
        modules = [
            "src",
            "src.models",
            "src.video_source",
            "src.calibration",
            "src.motion_gate",
            "src.segmentation",
            "src.card_detector",
            "src.rank_recognizer",
            "src.table_tracker",
            "src.blackjack_rules",
            "src.hud",
            "src.pipeline",
        ]
        for mod_name in modules:
            with self.subTest(module=mod_name):
                mod = importlib.import_module(mod_name)
                self.assertIsNotNone(mod)

    def test_load_default_config(self) -> None:
        cfg = load_config(REPO_ROOT / "configs" / "default_config.yaml")
        expected_sections = {
            "canvas",
            "video",
            "calibration",
            "motion_gate",
            "segmentation",
            "card_detector",
            "rank_recognizer",
            "tracker",
            "hud",
        }
        self.assertTrue(expected_sections.issubset(cfg.keys()))
        self.assertEqual(
            (cfg["canvas"]["width"], cfg["canvas"]["height"]),
            CANONICAL_CANVAS_SIZE,
        )
        self.assertEqual(len(VALID_RANKS), 13)

    def test_table_calibration_json_roundtrip(self) -> None:
        calib = TableCalibration(
            canvas_width=1280,
            canvas_height=720,
            src_corners=[(10.0, 20.0), (1270.0, 20.0), (1270.0, 700.0), (10.0, 700.0)],
            homography=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            zones=[
                ZoneConfig(zone_id="DEALER", role="dealer", rect=(340, 40, 940, 280)),
                ZoneConfig(zone_id="P1", role="player", rect=(80, 360, 420, 680)),
                ZoneConfig(zone_id="P2", role="player", rect=(470, 360, 810, 680)),
                ZoneConfig(zone_id="P3", role="player", rect=(860, 360, 1200, 680)),
            ],
            green_bgr_mean=[42.5, 118.0, 35.2],
            hsv_green_lower=[35, 40, 40],
            hsv_green_upper=[90, 255, 255],
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_path = Path(tmp_dir) / "calibration.json"
            calib.save_json(out_path)
            loaded = TableCalibration.load_json(out_path)

        self.assertEqual(loaded, calib)

    def test_state_dataclasses_instantiation(self) -> None:
        det = CardDetection(
            zone_id="P1",
            centroid=(250.0, 500.0),
            bbox=(200, 430, 300, 570),
            angle_deg=0.0,
            status=CardStatus.FACE_UP,
            rank="A",
            confidence=0.94,
            corner_point=(210.0, 440.0),
        )
        tracked = TrackedCard(
            card_id=1,
            zone_id="P1",
            sub_hand_id="P1",
            centroid=det.centroid,
            bbox=det.bbox,
            status=det.status,
            rank=det.rank,
            confidence=det.confidence,
            first_seen_frame=10,
            last_seen_frame=10,
        )
        hand = HandState(
            hand_id="P1",
            zone_id="P1",
            role="player",
            cards=[tracked],
            score=11,
            is_soft=True,
            status=HandStatus.ACTIVE,
        )
        event = TableEvent(
            frame_idx=10,
            event_type=TableEventType.ADD,
            zone_id="P1",
            hand_id="P1",
            card_id=1,
            rank="A",
        )
        state = TableState(
            frame_idx=10,
            timestamp_sec=0.33,
            motion_state=MotionState.STABLE,
            hands={"P1": hand},
            recent_events=[event],
            fps=30.0,
        )
        serialized = state.to_dict()
        self.assertEqual(serialized["hands"]["P1"]["score"], 11)
        self.assertEqual(serialized["recent_events"][0]["event_type"], TableEventType.ADD)


if __name__ == "__main__":
    unittest.main()

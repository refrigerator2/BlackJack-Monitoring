"""Shared data contracts, enums, and configuration helpers for BlackJack-Monitoring."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Literal

import yaml

VALID_RANKS: tuple[str, ...] = (
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
)
CANONICAL_CANVAS_SIZE: tuple[int, int] = (1280, 720)


class CardStatus(str, Enum):
    """Visibility state of a detected or tracked card."""

    FACE_UP = "FACE_UP"
    FACE_DOWN = "FACE_DOWN"


class MotionState(str, Enum):
    """Stability state of the table ROI for motion-gated updates."""

    MOVING = "MOVING"
    SETTLING = "SETTLING"
    STABLE = "STABLE"


class HandStatus(str, Enum):
    """Blackjack evaluation status for a dealer or player hand."""

    EMPTY = "EMPTY"
    ACTIVE = "ACTIVE"
    BLACKJACK = "BLACKJACK"
    BUST = "BUST"
    STAND = "STAND"


class TableEventType(str, Enum):
    """Temporal state-transition events emitted by the table tracker."""

    ADD = "ADD"
    MOVE = "MOVE"
    REMOVE = "REMOVE"
    FLIP = "FLIP"
    SPLIT = "SPLIT"
    ROUND_RESET = "ROUND_RESET"


@dataclass
class ZoneConfig:
    """Rectangular table zone on the canonical warped canvas."""

    zone_id: str
    role: Literal["dealer", "player"]
    rect: tuple[int, int, int, int]

    def to_dict(self) -> dict[str, Any]:
        """Serialize zone configuration to a JSON-compatible dictionary."""
        return {
            "zone_id": self.zone_id,
            "role": self.role,
            "rect": list(self.rect),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ZoneConfig:
        """Deserialize zone configuration from a dictionary."""
        x1, y1, x2, y2 = data["rect"]
        return cls(
            zone_id=str(data["zone_id"]),
            role=data["role"],
            rect=(int(x1), int(y1), int(x2), int(y2)),
        )


@dataclass
class TableCalibration:
    """4-point homography calibration and table zone definitions."""

    canvas_width: int
    canvas_height: int
    src_corners: list[tuple[float, float]]
    homography: list[list[float]]
    zones: list[ZoneConfig]
    green_bgr_mean: list[float] | None = None
    hsv_green_lower: list[int] | None = None
    hsv_green_upper: list[int] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize calibration to a JSON-compatible dictionary."""
        return {
            "canvas_width": self.canvas_width,
            "canvas_height": self.canvas_height,
            "src_corners": [[float(x), float(y)] for x, y in self.src_corners],
            "homography": [[float(v) for v in row] for row in self.homography],
            "zones": [z.to_dict() for z in self.zones],
            "green_bgr_mean": (
                [float(v) for v in self.green_bgr_mean]
                if self.green_bgr_mean is not None
                else None
            ),
            "hsv_green_lower": (
                [int(v) for v in self.hsv_green_lower]
                if self.hsv_green_lower is not None
                else None
            ),
            "hsv_green_upper": (
                [int(v) for v in self.hsv_green_upper]
                if self.hsv_green_upper is not None
                else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TableCalibration:
        """Deserialize calibration from a dictionary."""
        return cls(
            canvas_width=int(data["canvas_width"]),
            canvas_height=int(data["canvas_height"]),
            src_corners=[(float(x), float(y)) for x, y in data["src_corners"]],
            homography=[[float(v) for v in row] for row in data["homography"]],
            zones=[ZoneConfig.from_dict(z) for z in data["zones"]],
            green_bgr_mean=(
                [float(v) for v in data["green_bgr_mean"]]
                if data.get("green_bgr_mean") is not None
                else None
            ),
            hsv_green_lower=(
                [int(v) for v in data["hsv_green_lower"]]
                if data.get("hsv_green_lower") is not None
                else None
            ),
            hsv_green_upper=(
                [int(v) for v in data["hsv_green_upper"]]
                if data.get("hsv_green_upper") is not None
                else None
            ),
        )

    def save_json(self, path: str | Path) -> None:
        """Write calibration data to a JSON file."""
        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(self.to_dict(), indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load_json(cls, path: str | Path) -> TableCalibration:
        """Load calibration data from a JSON file."""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)


@dataclass
class CardDetection:
    """Single-frame card candidate produced by CardDetector and RankRecognizer."""

    zone_id: str
    centroid: tuple[float, float]
    bbox: tuple[int, int, int, int]
    angle_deg: float
    status: CardStatus
    rank: str | None = None
    confidence: float = 0.0
    corner_point: tuple[float, float] | None = None
    cluster_id: int = 0


@dataclass
class TrackedCard:
    """Persistently tracked card across video frames."""

    card_id: int
    zone_id: str
    sub_hand_id: str
    centroid: tuple[float, float]
    bbox: tuple[int, int, int, int]
    status: CardStatus
    rank: str | None
    confidence: float
    first_seen_frame: int
    last_seen_frame: int
    missed_stable_frames: int = 0


@dataclass
class HandState:
    """Current Blackjack hand state for a dealer or player (sub-)stack."""

    hand_id: str
    zone_id: str
    role: Literal["dealer", "player"]
    cards: list[TrackedCard] = field(default_factory=list)
    score: int = 0
    is_soft: bool = False
    status: HandStatus = HandStatus.EMPTY
    is_split_hand: bool = False


@dataclass
class TableEvent:
    """Discrete state change emitted by TableTracker."""

    frame_idx: int
    event_type: TableEventType
    zone_id: str
    hand_id: str
    card_id: int | None = None
    rank: str | None = None
    details: str = ""


@dataclass
class TableState:
    """Complete table snapshot returned by the pipeline for each processed frame."""

    frame_idx: int
    timestamp_sec: float
    motion_state: MotionState
    hands: dict[str, HandState] = field(default_factory=dict)
    recent_events: list[TableEvent] = field(default_factory=list)
    fps: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize table state for logging or dataset evaluation."""
        return asdict(self)


def load_config(path: str | Path) -> dict[str, Any]:
    """Load YAML pipeline configuration into a plain dictionary."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in config file: {path}")
    return data

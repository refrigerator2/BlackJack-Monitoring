# Blackjack Table State Monitoring — Project Roadmap

**Course:** PSIO (Przetwarzanie Sygnałów i Obrazów / Signal and Image Processing)  
**Repository:** `BlackJack-Monitoring`  
**Team:** Yurii Sladkovskyi (`258498`), Ivan Kharytonov (`258480`), Tsimur Makarevich (`258483`)  
**Target Grade:** **5.0** (full Blackjack monitoring + Split support + live DroidCam demo)  
**Hard Constraint:** **100% Classical Computer Vision** — strictly **no** neural networks, deep learning, CNNs, YOLO, or ML-based OCR.

---

## 1. Project Overview & Locked Design Decisions

The goal is to build a real-time, deterministic computer vision system that monitors a physical Blackjack table from both **pre-recorded gameplay videos (`.mp4`)** and a **live camera feed (DroidCam)** over a uniform green table surface.

### Locked Architectural Decisions
| Area | Decision | Rationale |
| :--- | :--- | :--- |
| **Card Deck** | Single standardized deck design (multiple identical copies); **13 unique ranks** (`A, 2–10, J, Q, K`); **suits ignored**. | Suits do not affect Blackjack scoring. Calibrated templates from the exact deck maximize Normalized Cross-Correlation (NCC) accuracy without ML. |
| **Table Layout & Camera** | Rectangular table layout (**Dealer row at top**, **≥3 Player zones in bottom row**) + fixed overhead camera with **4-point homography calibration**. | Eliminates perspective distortion, standardizes card pixel scale across the table, and prevents adjacent player stacks from mixing. |
| **Overlap & Temporal Strategy** | **Hybrid architecture**: shingled/cascaded card dealing (corner index remains visible) + **motion-gated stable-frame change detection** + **temporal stack memory**. | Pure single-frame contour detection fails on overlapping stacks. Combining corner-index recognition with temporal state memory robustly tracks additions, moves, removals, flips, and **Splits** without double-counting. |
| **Face-Down Cards** | Detected and tracked as `FACE_DOWN` placeholders; value is ignored until flipped face-up. | Explicitly required by the project specification (`Monitorowanie stanu stołu w grze karcianej.pdf`). |
| **Runtime Environment** | Conda env `psio` (`Python 3.11.17`, `OpenCV 5.0.0`, `NumPy`, `SciPy`, `scikit-image`, `matplotlib`). | Matches course lab stack; fast vectorized C++/OpenCV operations easily achieve real-time FPS on CPU. |

---

## 2. Grading Criteria Traceability (Target: 5.0)

Every criterion from `Monitorowanie stanu stołu w grze karcianej.pdf` maps directly to a concrete module and verification gate:

| # | Grading Criterion | Responsible Pipeline Module | Target Milestone | Verification Metric |
| :-: | :--- | :--- | :---: | :--- |
| 1 | **Card Detection** (incl. partial overlap) | `segmentation.py`, `card_detector.py` | M2, M3 | ≥95% detection recall on isolated & shingled stacks |
| 2 | **13-Rank Recognition** (`A, 2–10, J, Q, K`) | `rank_recognizer.py` | M2 | ≥95% rank accuracy across all 13 ranks (incl. `10`, `6/9`, `J/Q/K`) |
| 3 | **Algorithm Robustness** (position, orientation, partial occlusion) | `calibration.py`, `card_detector.py`, `motion_gate.py` | M3, M4 | Correct recognition at arbitrary rotations & during hand occlusions |
| 4 | **Table State Grouping** (Dealer + ≥3 Players) | `calibration.py`, `table_tracker.py` | M1, M4 | 100% correct zone assignment for Dealer & Players 1–3+ |
| 5 | **Blackjack Scoring** (Soft/Hard Ace `1` or `11`) | `blackjack_rules.py` | M5 | 100% unit-test pass rate on all Ace/Bust/Blackjack edge cases |
| 6 | **Video Frame-by-Frame Processing** | `video_source.py`, `pipeline.py` | M1, M4 | Continuous end-to-end processing of full `.mp4` rounds |
| 7 | **Implementation Quality, FPS & Visualization** | `hud.py`, `pipeline.py` | M6 | ≥15–25 FPS on CPU, modular code, clear real-time HUD overlay |
| 8 | **Temporal State Monitoring** (add, move, remove; no double-counting) | `table_tracker.py` | M4 | Zero duplicate card counts across full multi-event test videos |
| 9 | **Split Handling** *(mandatory for 5.0)* | `table_tracker.py`, `blackjack_rules.py` | M5 | Automatic split of equal-rank pair into 2 independent sub-stacks |
| 10 | **Final Report** (WIKAMP DOCX template) | `PSIO-raport-draft.docx` → final DOCX | M7 | Complete Sections 1–6 with real metrics, plots, and failure cases |
| 11 | **Final Presentation + Live Demo** | Live DroidCam mode + recorded fallback | M7 | Stable live demo on green mat in classroom lighting |

---

## 3. Reuse of Previous PSIO Laboratory Techniques

This project directly synthesizes classical techniques practiced in `lab1`–`lab7` and `praca_domowa`:

| Lab / Homework | Practiced Techniques | Direct Application in `BlackJack-Monitoring` |
| :--- | :--- | :--- |
| **Lab 1** (`lab1.ipynb`, `lab1_z2.ipynb`) | Matrix slicing, geometric rotations, affine transforms | Corner ROI cropping, card patch rotation (`0°`/`180°` alignment), homography warping |
| **Lab 2** (`lab2.ipynb`) | Histograms, contrast stretching, gamma correction, LUTs | Illumination normalization before template matching, fast intensity LUTs for glare suppression |
| **Lab 3 & PD 3** (`lab3.ipynb`, `praca-domowa-3.ipynb`) | Global/adaptive thresholding, RGB color distance, HSV `cv2.inRange`, `regionprops` | White card-stock vs. green felt segmentation, geometric filtering (area, solidity, aspect ratio) |
| **Lab 4** (`lab4.ipynb`) | Gaussian, median, and Vector Median Filter (VMF) denoising | Suppressing DroidCam compression noise & specular salt-and-pepper artifacts before edge detection |
| **Lab 5 & PD 5** (`lab5.ipynb`, `praca_domowa_5.ipynb`) | 2D FFT frequency-domain filtering & fast FFT-based 2D convolution (`apply_mask_with_fft`) | Optional frequency-domain correlation speedup for large templates and periodic card-back texture diagnostics |
| **Lab 6** (`lab6.ipynb`) | `threshold_triangle`, Canny edges, `clear_border`, morphological closing, `measure.label`, shape filtering | Clean binary card masks, closing gaps caused by pips/indices near borders, separating valid card blobs |
| **Lab 7** (`lab7.ipynb`, `Snooker2.mp4`) | `VideoCapture`/`VideoWriter`, green playfield mask (`connectedComponentsWithStats` + `floodFill` + `erode`), fast BGR color-distance foreground segmentation via `absdiff` + squared LUT (`SQ_LUT_8`), `distanceTransform` local-maxima splitting, LAB descriptors, Hungarian assignment (`scipy.optimize.linear_sum_assignment`) + occlusion grace window, HUD overlays | **Core blueprint** for our system: green-table masking, vectorized `absdiff`+LUT reused for both foreground segmentation and motion gating, touching-card separation via distance transform, LAB color descriptors for face-down detection, Hungarian card tracking across moves/occlusions, and real-time HUD rendering |

---

## 4. Pure-CV System Architecture

```text
[Video File (.mp4) / Live DroidCam]
                │
                ▼
┌───────────────────────────────────────────┐
│ Stage 1: Calibration & Table Homography   │  4-point warpPerspective -> fixed top-down canvas
│ (calibration.py)                          │  Defines Dealer zone + Player 1..N zones
└───────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ Stage 2: Motion Gate & Hand Occlusion     │  BGR absdiff + squared LUT (Lab 7)
│ (motion_gate.py)                          │  States: MOVING -> SETTLING -> STABLE (N frames)
└───────────────────────────────────────────┘
                │ (Only commit state updates on STABLE frames)
                ▼
┌───────────────────────────────────────────┐
│ Stage 3: Green-Felt Mask & Segmentation   │  HSV/LAB green subtraction + morph open/close
│ (segmentation.py)                         │  Separates foreground blobs per table zone
└───────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ Stage 4: Card & Corner-Index Localization │  Isolated cards: minAreaRect / 4-corner warp
│ (card_detector.py)                        │  Shingled stacks: visible corner detection +
│                                           │  distanceTransform / edge-corner geometry
│                                           │  Face-down check: interior LAB/variance test
└───────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ Stage 5: 13-Rank Template Recognition     │  CLAHE / zero-mean normalization
│ (rank_recognizer.py)                      │  Multi-angle NCC (TM_CCOEFF_NORMED) vs 13 templates
│                                           │  Disambiguation: '10' width, '6'/'9' orientation,
│                                           │  J/Q/K secondary correlation / projection profile
└───────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ Stage 6: Temporal Tracker & Split Engine  │  Per-zone stack memory + Hungarian matching
│ (table_tracker.py, blackjack_rules.py)    │  Events: ADD, MOVE, REMOVE, FLIP, SPLIT
│                                           │  Scoring: Soft/Hard Ace (1/11), Bust, Blackjack
└───────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ Stage 7: Real-Time HUD & Output Writer    │  Zone boxes, card labels, scores, Split badges,
│ (hud.py)                                  │  FPS, stability indicator, optional debug view
└───────────────────────────────────────────┘
```

### Key Algorithmic Details

1. **Motion Gating (Zero Hand-Corruption):**
   - Compute frame-to-frame difference on the warped table ROI using fast BGR `absdiff` (Lab 7).
   - If changed pixel ratio exceeds `MOTION_THRESH`, mark table (or specific zone) as `MOVING` and freeze the displayed game state.
   - Require `K` consecutive low-motion frames (e.g., `K = 5–8`, ~0.2–0.3 s) before declaring `STABLE` and running state-commit logic. This prevents half-dealt cards or hovering hands from triggering false detections.
2. **Face-Up vs. Face-Down Classification:**
   - Standard playing cards have a bright, low-saturation white border/corner (`L*` high, `S` low in HSV/LAB), whereas card backs have high saturation or high-frequency textured patterns across the full rectangle.
   - Measure border/corner mean brightness and saturation inside each candidate card region; classify as `FACE_DOWN` when white-border criteria fail, and track its centroid until flipped.
3. **Handling Overlapping (Shingled) Cards:**
   - **Primary path (visible corner index):** In Blackjack, cards in a stack are dealt in a cascaded/shingled fan so the top-left (or bottom-right) rank index of each card remains unobstructed. We detect candidate card corners along the outer contour of each foreground cluster (convex hull vertices, right-angle corner pairs via `goodFeaturesToTrack` / contour polygonal approximation, and `distanceTransform` ridges), orient each corner patch along its local card edge vector, and run NCC against the 13 calibrated rank templates.
   - **Secondary path (temporal diffing):** When a new card is placed on an existing stack, the pixel difference between the previous `STABLE` frame and the current `STABLE` frame isolates the newly exposed card region directly, even when partial occlusion alters the cluster's global contour.
4. **Disambiguating Hard Rank Pairs (Pure CV):**
   - **`10` vs `0`/`1`:** `10` is a two-character glyph with a distinctly wider bounding box aspect ratio; match the full `"10"` composite template and verify glyph width ratio.
   - **`6` vs `9`:** Always orient the corner ROI consistently relative to the card's inward vector (from corner toward card interior) so `6` and `9` are never rotated `180°` into each other.
   - **`J` vs `Q` vs `K`:** Use high-resolution calibrated templates of the exact deck plus secondary check on horizontal/vertical ink projection profiles if the top-2 NCC scores are within a small margin (`Δ < 0.05`).
5. **Split Detection (Grade 5.0 Requirement):**
   - Eligible trigger: A player zone holds **2 face-up cards of equal rank** (or equal Blackjack value if casino rules allow, configurable; default: exact same rank, e.g., `8 + 8` or `A + A`).
   - Trigger event: After a `MOVING → STABLE` transition, the single foreground cluster in that player zone separates into **two spatially distinct clusters/cards** whose centroids exceed `SPLIT_MIN_DIST_PX` (and each matches one of the original pair's ranks).
   - State transition: The player zone spawns two independent sub-stacks (`P{i}-L` and `P{i}-R`), each with its own spatial bounding region, card list, and independent Blackjack score calculation. Subsequent cards dealt to either sub-stack are assigned by nearest-sub-stack proximity.

---

## 5. Proposed Repository Structure

```text
BlackJack-Monitoring/
├── roadmap.md                    # This document
├── README.md                     # Setup, usage, CLI commands, demo instructions
├── requirements.txt              # opencv-python, numpy, scipy, scikit-image, matplotlib, pytest
├── configs/
│   ├── default_config.yaml       # Thresholds, HSV green bounds, motion gate, Split params
│   └── calibration.json          # Saved 4-point homography & Dealer/Player zone polygons
├── assets/
│   └── templates/                # Calibrated 13-rank grayscale templates (A.png .. K.png)
├── src/
│   ├── __init__.py
│   ├── video_source.py           # Unified .mp4 & DroidCam (index / HTTP MJPEG / RTSP) reader
│   ├── calibration.py            # Interactive 4-point table homography & zone ROI tool
│   ├── motion_gate.py            # Per-zone/global motion detection & STABLE hysteresis
│   ├── segmentation.py           # Green felt HSV/LAB masking & morphological cleanup
│   ├── card_detector.py          # Isolated & shingled card/corner localization + face-down check
│   ├── rank_recognizer.py        # 13-rank NCC template matcher + disambiguation rules
│   ├── table_tracker.py          # Temporal memory, Hungarian matching, ADD/MOVE/REMOVE/FLIP/SPLIT
│   ├── blackjack_rules.py        # Soft/Hard Ace scoring, Bust, Blackjack, Split sub-hand logic
│   ├── hud.py                    # Real-time OpenCV overlay & debug multi-panel view
│   └── pipeline.py               # Main frame loop tying all stages together
├── scripts/
│   ├── calibrate_table.py        # CLI tool to click 4 corners & define zones on live/video frame
│   ├── capture_templates.py      # Semi-automated tool to crop & save the 13 rank templates
│   ├── run_monitor.py            # Main entry point (--video path.mp4 | --camera url/index)
│   └── evaluate_dataset.py       # Benchmarks accuracy & FPS against ground-truth JSON timelines
├── tests/
│   ├── test_blackjack_rules.py   # Unit tests for scoring, Aces, Bust, Blackjack, Split
│   ├── test_table_tracker.py     # Unit tests for ADD/MOVE/REMOVE/FLIP/SPLIT without double-count
│   └── test_rank_recognizer.py   # Template matching unit tests on synthetic rotated/noisy crops
└── data/                         # (gitignored) Recorded test videos & ground-truth JSON annotations
```

---

## 6. Phased Implementation Plan (Milestones M0–M7)

Suggested parallel ownership across the 3-person team:
- **Track A (Camera, Calibration & Segmentation):** `video_source.py`, `calibration.py`, `segmentation.py`, `motion_gate.py`
- **Track B (Card Localization & 13-Rank Recognition):** `card_detector.py`, `rank_recognizer.py`, `capture_templates.py`
- **Track C (Temporal Tracking, Blackjack Rules, Split & HUD):** `table_tracker.py`, `blackjack_rules.py`, `hud.py`, `evaluate_dataset.py`

### M0 — Setup, Physical Rig & Test Video Capture
- [x] Initialize Python package structure (`src/`, `scripts/`, `tests/`, `configs/`, `.gitignore` for large `.mp4` files).
- [ ] Prepare physical setup: uniform matte green felt/mat, fixed overhead mount for smartphone (DroidCam), diffuse lighting (minimize glare on laminated cards).
- [ ] Capture calibration reference image + clean top-down photo of all **13 ranks** (`A, 2–10, J, Q, K`) from the chosen deck.
- [ ] Record a standardized **6-video test suite** (1080p or 720p, 30 FPS):
  1. `01_single_cards.mp4` — isolated cards placed at varied positions & orientations (`0°–360°`).
  2. `02_shingled_deal.mp4` — full round with Dealer + 3 Players using shingled/cascaded overlaps.
  3. `03_facedown_flip.mp4` — Dealer hole card dealt face-down, later flipped face-up.
  4. `04_move_remove.mp4` — cards nudged, moved between zones, and cleared at end of round.
  5. `05_split_round.mp4` — Player dealt a pair (e.g., `8-8`), splits into two independent stacks, receives hits on both.
  6. `06_stress_lighting.mp4` — minor hand shadows, rapid dealing, multi-card bust/blackjack edge cases.

### M1 — Video I/O, Homography Calibration & Green-Table Masking
- [ ] Implement `video_source.py` supporting `.mp4` files, USB webcams, and DroidCam (MJPEG/HTTP URL or virtual webcam index).
- [ ] Implement `scripts/calibrate_table.py`: click 4 table corners → compute & save homography matrix (`calibration.json`) + interactive/configurable rectangular zones (`Dealer`, `Player 1`, `Player 2`, `Player 3`, expandable).
- [ ] Implement `segmentation.py`: HSV + LAB green background model (inspired by Lab 7), auto-calibrated from empty-table frames, plus morphological cleanup (`open`/`close`).
- **Exit Gate:** Warped top-down table stream runs at ≥30 FPS with clean binary foreground masks for cards on green felt.

### M2 — Isolated Card Detection & 13-Rank Recognition
- [ ] Implement `scripts/capture_templates.py` to extract standardized, normalized grayscale templates for `A, 2–10, J, Q, K`.
- [ ] Implement isolated card contour detection (`findContours`, `minAreaRect`, perspective rectification) and corner-index ROI extraction.
- [ ] Implement `rank_recognizer.py` using normalized `cv2.matchTemplate(..., cv2.TM_CCOEFF_NORMED)` with rotation alignment and `10` / `6-9` / `J-Q-K` disambiguation.
- **Exit Gate:** ≥98% rank accuracy on `01_single_cards.mp4` across all 13 ranks and arbitrary rotations.

### M3 — Face-Down Detection & Shingled/Overlapping Stack Extraction
- [ ] Add face-down card classifier (border whiteness + interior saturation/variance check) so face-down cards are localized and labeled `HIDDEN` rather than misclassified as random ranks.
- [ ] Extend `card_detector.py` to extract visible corner indices from overlapping/shingled clusters (contour corner geometry + edge-aligned corner patches + `distanceTransform` peak assistance).
- [ ] Validate on `02_shingled_deal.mp4` and `03_facedown_flip.mp4`.
- **Exit Gate:** ≥95% detection and rank accuracy on shingled 2–5 card stacks and 100% accurate face-down detection.

### M4 — Motion Gating & Temporal State Machine (No Double-Counting)
- [ ] Implement `motion_gate.py` with per-zone and global motion energy + `MOVING → SETTLING → STABLE` hysteresis.
- [ ] Implement `table_tracker.py`:
  - Stable-frame diffing to isolate newly added cards on top of existing stacks.
  - Hungarian assignment (`scipy.optimize.linear_sum_assignment`) to match existing cards across frames and handle small nudges/moves without creating duplicates.
  - Confirmation window (`N` stable frames) before committing `ADD`, `REMOVE`, `MOVE`, or `FLIP` (`FACE_DOWN → FACE_UP`).
  - Round-reset detection when table is cleared.
- **Exit Gate:** Zero double-counting on `02_shingled_deal.mp4`, `03_facedown_flip.mp4`, and `04_move_remove.mp4`.

### M5 — Blackjack Rules Engine & Full Split Support (Grade 5.0 Gate)
- [ ] Implement `blackjack_rules.py`:
  - Soft vs. Hard Ace computation (`A` = 11 unless total > 21, then 1; handles multiple Aces cleanly, e.g., `A + A + 9 = 21`).
  - Hand statuses: `ACTIVE`, `BLACKJACK` (natural 21 on 2 cards), `BUST` (>21), `STAND` / Dealer `17+`.
  - Independent sub-hand scoring for split hands.
- [ ] Implement Split detection in `table_tracker.py` (equal-rank pair separating into 2 spatial clusters → spawn `P{i}-L` and `P{i}-R` sub-stacks).
- [ ] Write comprehensive `pytest` unit tests (`test_blackjack_rules.py`, `test_table_tracker.py`).
- **Exit Gate:** 100% unit tests passing + end-to-end pass on `05_split_round.mp4`.

### M6 — Real-Time Optimization, Live DroidCam Hardening & Quantitative Evaluation
- [ ] Profile pipeline; optimize hot paths (ROI-only processing per zone, downscaled motion mask, pre-computed template pyramids/rotations) to maintain **≥15–25 FPS** live.
- [ ] Add live demo conveniences: single-key recalibration of green-felt HSV thresholds (`c` key), instant round reset (`r` key), debug mask split-screen toggle (`d` key), and automatic video recording of live runs.
- [ ] Implement `scripts/evaluate_dataset.py` to compute quantitative metrics on the 6-video test suite (detection precision/recall, per-rank confusion matrix, event accuracy, Split success rate, mean FPS) for Report Section 3 & 4.

### M7 — Final Report & Presentation Rehearsal
- [ ] Complete `PSIO-raport-draft.docx` → final report (`2. MATERIAŁY I METODY` with architecture block diagram, `3. REZULTATY` with confusion matrix & qualitative frames, `4. OGRANICZENIA METODY` with real failure cases, `5. WNIOSKI`).
- [ ] Prepare presentation slides + live DroidCam demo checklist (green mat, tripod, USB/Wi-Fi DroidCam tether, backup `.mp4` videos ready in case of classroom Wi-Fi issues).

---

## 7. Key Technical Risks & Mitigations

| Risk | Impact | Pure-CV Mitigation |
| :--- | :--- | :--- |
| **Specular glare** on glossy laminated cards | Washes out rank ink, breaks NCC | Use matte/linen-finish cards if possible; diffuse lighting; CLAHE/local contrast normalization; HSV saturation/value glare guard |
| **Classroom lighting shift** during live demo | Static HSV green thresholds fail | Live background-sampling hotkey (`c`) to re-estimate green felt HSV/LAB mean & std from an empty table in 1 second |
| **Heavy overlap** hiding a card's corner index | Single-frame detector misses the occluded card | Temporal stack memory retains previously confirmed cards even if later partially covered, until the entire cluster is removed |
| **Card nudging mistaken for Split** | False Split creation | Require (a) exactly 2 cards of equal rank, (b) clear green-felt gap between two distinct contours, and (c) centroid separation `> SPLIT_MIN_DIST_PX` |
| **`6` vs `9` or `10` misread** | Wrong hand score | Consistent inward-facing corner orientation for `6`/`9`; composite width-aware template + aspect ratio check for `10` |
| **DroidCam Wi-Fi lag / compression** | Frame drops or blurry edges | Prefer **USB tether** via DroidCam for the live presentation; set camera focus/exposure lock (`AE/AF lock`) |

---

## 8. Verification & Testing Plan

1. **Automated Unit Tests (`pytest`):**
   - `test_blackjack_rules.py`: Soft/Hard Aces (single, double, triple Aces), natural Blackjack vs. 3-card 21, Bust, Split sub-hand scoring, face-down card exclusion from visible score.
   - `test_table_tracker.py`: Synthetic event sequences verifying `ADD`, `MOVE`, `REMOVE`, `FLIP`, `SPLIT`, hand-occlusion freeze, and zero double-counting.
   - `test_rank_recognizer.py`: All 13 templates tested under synthetic rotation (`±15°`), brightness shifts (`±25%`), and Gaussian blur.
2. **Recorded Video Regression Suite:**
   - Run `scripts/evaluate_dataset.py` across all 6 annotated `.mp4` videos before every major milestone merge and before the final presentation.
3. **Live Demo Dry-Run:**
   - Full rehearsal with DroidCam over USB + green mat under non-ideal indoor lighting, testing a complete multi-player round including a face-down Dealer hole card and a Player Split.

---

## 9. Interfaces & Data Contracts (For Parallel Development)

All modules in `src/` communicate exclusively through the typed contracts defined in `src/models.py` and the configuration schema in `configs/default_config.yaml`. Agents working on Tracks A, B, and C in parallel **must not** invent ad-hoc dictionaries or alter these conventions without updating `src/models.py` first.

### Global Conventions
- **Canonical Warped Canvas:** `1280 × 720` (`CANONICAL_CANVAS_SIZE = (1280, 720)`).
- **Coordinate System:** OpenCV `(x, y)` pixel coordinates (`x` = column `0..1279`, `y` = row `0..719`). Bounding boxes use `(x1, y1, x2, y2)` (`int`).
- **Image Format:** `BGR` `uint8` `np.ndarray` (`shape = (720, 1280, 3)`). Binary masks use `uint8` (`0` = background, `255` = foreground).
- **Zone & Hand Identifiers:**
  - Dealer zone & hand ID: `"DEALER"`.
  - Player zone IDs: `"P1"`, `"P2"`, `"P3"` (expandable to `"P4"`, ...).
  - After a Split in zone `P{i}`, sub-hand IDs become `"P{i}-L"` and `"P{i}-R"`.
- **Valid Ranks:** `VALID_RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")`.

### Core Data Contracts (`src/models.py`)
- **Enums (`str, Enum`):**
  - `CardStatus`: `FACE_UP`, `FACE_DOWN`
  - `MotionState`: `MOVING`, `SETTLING`, `STABLE`
  - `HandStatus`: `EMPTY`, `ACTIVE`, `BLACKJACK`, `BUST`, `STAND`
  - `TableEventType`: `ADD`, `MOVE`, `REMOVE`, `FLIP`, `SPLIT`, `ROUND_RESET`
- **Dataclasses:**
  - `ZoneConfig(zone_id, role, rect)` — `role` in `{"dealer", "player"}`, `rect = (x1, y1, x2, y2)` on canonical canvas.
  - `TableCalibration(canvas_width, canvas_height, src_corners, homography, zones, green_bgr_mean, hsv_green_lower, hsv_green_upper)` — JSON-serializable via `save_json` / `load_json`.
  - `CardDetection(zone_id, centroid, bbox, angle_deg, status, rank=None, confidence=0.0, corner_point=None, cluster_id=0)` — per-frame detector output.
  - `TrackedCard(card_id, zone_id, sub_hand_id, centroid, bbox, status, rank, confidence, first_seen_frame, last_seen_frame, missed_stable_frames=0)` — persistent tracked card.
  - `HandState(hand_id, zone_id, role, cards, score=0, is_soft=False, status=HandStatus.EMPTY, is_split_hand=False)` — evaluated hand state.
  - `TableEvent(frame_idx, event_type, zone_id, hand_id, card_id=None, rank=None, details="")` — discrete timeline event.
  - `TableState(frame_idx, timestamp_sec, motion_state, hands, recent_events, fps=0.0)` — full frame snapshot passed to `HUDRenderer`.

### Configuration Schemas
- **`configs/default_config.yaml`** top-level sections: `canvas`, `video`, `calibration`, `motion_gate`, `segmentation`, `card_detector`, `rank_recognizer`, `tracker`, `hud`. Loaded via `src.models.load_config(path)`.
- **`configs/calibration.json`** schema (produced by `scripts/calibrate_table.py`, loaded by `TableCalibration.load_json`):
  ```json
  {
    "canvas_width": 1280,
    "canvas_height": 720,
    "src_corners": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
    "homography": [[...], [...], [...]],
    "zones": [
      {"zone_id": "DEALER", "role": "dealer", "rect": [x1, y1, x2, y2]},
      {"zone_id": "P1", "role": "player", "rect": [x1, y1, x2, y2]}
    ],
    "green_bgr_mean": [b, g, r],
    "hsv_green_lower": [h, s, v],
    "hsv_green_upper": [h, s, v]
  }
  ```

### Module Interface Table

| Module | Track | Primary Class / Functions | Inputs | Outputs |
| :--- | :---: | :--- | :--- | :--- |
| `src/video_source.py` | A | `VideoSource.read()`, `fps`, `frame_size` | Video path / DroidCam URL or index | `(ok: bool, frame_bgr \| None)` |
| `src/calibration.py` | A | `compute_homography()`, `warp_table()`, `build_default_zones()` | Raw `frame_bgr`, `TableCalibration` | Canonical `1280×720` `warped_bgr`, `list[ZoneConfig]` |
| `src/motion_gate.py` | A | `MotionGate.update(warped_bgr)`, `reset()` | Canonical `warped_bgr` | `MotionState` (`MOVING`/`SETTLING`/`STABLE`) |
| `src/segmentation.py` | A | `TableSegmenter.calibrate_background()`, `segment_foreground()`, `extract_zone_mask()` | `warped_bgr`, `ZoneConfig` | Binary `uint8` mask (`0`/`255`) |
| `src/card_detector.py` | B | `CardDetector.detect_in_zone()`, `is_face_down()` | `warped_bgr`, `zone_mask`, `ZoneConfig` | `list[CardDetection]` |
| `src/rank_recognizer.py` | B | `RankRecognizer.load_templates()`, `recognize_corner()` | Rectified corner patch `BGR` | `(rank: str \| None, ncc_score: float)` |
| `src/table_tracker.py` | C | `TableTracker.update()`, `reset_round()` | `frame_idx`, `MotionState`, `list[CardDetection]` | `TableState` |
| `src/blackjack_rules.py` | C | `evaluate_hand(ranks)`, `can_split(ranks)` | `list[str]` (face-up ranks) | `(score, is_soft, HandStatus)` / `bool` |
| `src/hud.py` | C | `HUDRenderer.render(warped_bgr, state, zones, debug_mask)` | `warped_bgr`, `TableState`, `list[ZoneConfig]` | Annotated `BGR` frame |
| `src/pipeline.py` | All | `BlackjackPipeline.process_frame()`, `recalibrate_background()`, `reset_round()` | Raw `frame_bgr`, `frame_idx`, `timestamp_sec` | `(TableState, annotated_bgr)` |

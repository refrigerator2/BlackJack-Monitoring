"""Pure Blackjack scoring rules (Soft/Hard Ace, Bust, Natural Blackjack, Split)."""

from __future__ import annotations

from src.models import HandStatus


def evaluate_hand(ranks: list[str]) -> tuple[int, bool, HandStatus]:
    """Compute (best_score, is_soft, hand_status) for a list of face-up card ranks."""
    raise NotImplementedError("TODO: Milestone M5")


def can_split(ranks: list[str], exact_rank_only: bool = True) -> bool:
    """Return True if a two-card hand is eligible for a Blackjack Split."""
    raise NotImplementedError("TODO: Milestone M5")

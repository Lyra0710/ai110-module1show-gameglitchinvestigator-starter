import os
import sys

import pytest

# Make app.py and logic_utils.py importable when running pytest from anywhere.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import check_guess, parse_guess
from logic_utils import new_game_state


# =====================================================================
# Bug 1: Higher / Lower hint was reversed
# ---------------------------------------------------------------------
# check_guess used to tell the player to "Go HIGHER!" when their guess
# was already too high (and "Go LOWER!" when too low). The hint must
# point toward the secret: too high -> go LOWER, too low -> go HIGHER.
# These tests assert the *direction of the message*, which is what the
# bug actually got wrong.
# =====================================================================

def test_correct_guess_is_a_win():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high_tells_player_to_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()


def test_guess_too_low_tells_player_to_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()


# =====================================================================
# Bug 2: "New Game" did not start a new game
# ---------------------------------------------------------------------
# The handler only reset attempts and secret. A stale "won"/"lost"
# status caused the app to st.stop() immediately, and score/history
# carried over. The secret was also drawn from a hardcoded 1..100,
# ignoring difficulty. new_game_state() now owns the full reset.
# =====================================================================

def test_new_game_resets_status_to_playing():
    """The core bug: a stale 'won'/'lost' status must be cleared."""
    state = new_game_state(1, 100)
    assert state["status"] == "playing"


def test_new_game_clears_score_and_history():
    state = new_game_state(1, 100)
    assert state["score"] == 0
    assert state["history"] == []


def test_new_game_resets_every_field():
    """Guard against a future field being added but forgotten in the reset."""
    state = new_game_state(1, 100)
    assert set(state.keys()) == {"attempts", "secret", "score", "status", "history"}


@pytest.mark.parametrize(
    "low, high",
    [
        (1, 20),   # Easy
        (1, 100),  # Normal
        (1, 50),   # Hard
    ],
)
def test_new_game_secret_respects_difficulty_range(low, high):
    """Secret must fall within the difficulty's range, not a hardcoded 1..100."""
    for _ in range(200):
        secret = new_game_state(low, high)["secret"]
        assert low <= secret <= high


# =====================================================================
# Bug 3: Attempt counter off-by-one / counted invalid input
# ---------------------------------------------------------------------
# Two parts to the fix:
#   (a) A new game starts at 0 attempts (it used to initialize to 1 on
#       first load while New Game reset to 0 -- an inconsistent start).
#   (b) The app only increments attempts inside the `else` branch, i.e.
#       only when parse_guess succeeds. So the counting now hinges on
#       parse_guess returning ok=False for invalid input (no attempt
#       spent) and ok=True for a real number (attempt spent).
# =====================================================================

def test_new_game_starts_at_zero_attempts():
    assert new_game_state(1, 100)["attempts"] == 0


@pytest.mark.parametrize("bad_input", [None, "", "abc", "1.2.3", "twelve"])
def test_invalid_input_is_rejected_so_no_attempt_is_spent(bad_input):
    ok, value, err = parse_guess(bad_input)
    assert ok is False
    assert value is None
    assert err is not None


def test_valid_integer_is_accepted_so_an_attempt_is_spent():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_valid_decimal_is_accepted_and_truncated():
    ok, value, err = parse_guess("3.9")
    assert ok is True
    assert value == 3
    assert err is None

import os
import sys

import pytest

# Make logic_utils importable when running pytest from anywhere.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import new_game_state


# The bug: the "New Game" button only reset `attempts` and `secret`. It left
# `status`, `score`, and `history` from the previous game in place. Because a
# stale "won"/"lost" status caused the app to immediately st.stop(), pressing
# "New Game" appeared to do nothing. It also drew the secret from 1..100,
# ignoring the difficulty range. new_game_state() now centralizes that reset;
# these tests pin down the behavior so the bug cannot silently return.


def test_new_game_resets_status_to_playing():
    """The core bug: a stale 'won'/'lost' status must be cleared."""
    state = new_game_state(1, 100)
    assert state["status"] == "playing"


def test_new_game_resets_score_and_history_and_attempts():
    """Score, history, and attempts must not carry over from the last game."""
    state = new_game_state(1, 100)
    assert state["score"] == 0
    assert state["history"] == []
    assert state["attempts"] == 0


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

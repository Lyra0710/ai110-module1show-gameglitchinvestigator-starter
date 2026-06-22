import random


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def new_game_state(low: int, high: int):
    """
    Return the fresh game state for starting a new game.

    Every field is reset so a new game does not carry over the previous
    game's status, score, or history. The secret is drawn from the
    [low, high] range for the current difficulty.
    """
    return {
        "attempts": 0,
        "secret": random.randint(low, high),
        "score": 0,
        "status": "playing",
        "history": [],
    }

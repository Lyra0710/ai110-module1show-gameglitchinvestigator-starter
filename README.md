# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ Game Glitch Investigator is a Streamlit-based number guessing game used as a debugging exercise. The player picks a difficulty (Easy, Normal, or Hard), and the app generates a secret number within that difficulty's range. On each guess, the game gives a "Too High" / "Too Low" hint to steer the player toward the secret, tracks attempts against a per-difficulty limit, and updates a running score until the player either guesses correctly or runs out of attempts. The real purpose of the project, though, is to investigate and repair an intentionally broken AI-generated app. Finding and fixing logic and Streamlit state bugs (reversed hints, miscounted attempts, a "New Game" button that doesn't reset, and a secret that resets on every click), then refactoring the logic into logic_utils.py and verifying the fixes with pytest.]
- [
1. Reversed Higher/Lower hints. When a guess was too high the game said "Go HIGHER!" and when it was too low it said "Go LOWER!" — the hints pointed the wrong way, making the game impossible to win by following them. (in check_guess)

2. Attempt counter bugs. The counter started at 1 on first load but reset to 0 on New Game (inconsistent start), and it was incremented before the input was validated — so typing something invalid like abc still cost the player an attempt.

3. "New Game" didn't start a new game. The button only reset attempts and secret, leaving a stale "won"/"lost" status in session state. Because the script reran from the top and hit that stale status, the game immediately stopped with "You already won." Score and history also carried over.

4. New Game ignored difficulty. The secret on a new game was drawn from a hardcoded 1–100 instead of the selected difficulty's range, so on Easy/Hard it could be outside the displayed range.] 
- [ 1. Corrected the hint direction. In check_guess, I swapped the messages so a too-high guess now says "Go LOWER!" and a too-low guess says "Go HIGHER!", so the hints point toward the secret.

2. Fixed attempt counting. I set the starting value to 0 so it matches the New Game reset, and moved the attempts += 1 increment into the valid-guess branch (after parse_guess succeeds). Now invalid input shows an error without spending an attempt.

3. Made "New Game" actually reset. I extracted the reset into a new_game_state(low, high) function in logic_utils.py that returns a fresh attempts, secret, score, status, and history, and wired the button to apply it with st.session_state.update(...). Resetting status back to "playing" is what fixed the game getting stuck on "You already won."

4. Made New Game respect difficulty. The new secret is now drawn from random.randint(low, high) for the selected difficulty instead of a hardcoded 1–100.
] 

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Game starts. The secret (63) is generated within the Normal range, and the player has 8 attempts.
2. Invalid input is rejected. Typing abc shows an error and is logged to history, but the attempt counter does not decrease — this is the attempt-counting fix in action.
3. First real guess (40). 40 < 63, so the game correctly returns "Too Low" with the hint "Go HIGHER!" — the hint now points the right direction.
4. Second guess (70). 70 > 63, so it returns "Too High" with "Go LOWER!".
5. Winning guess (63). Outcome is "Win", balloons fire, and the game reports the secret and final score, then sets status to "won".
6. New Game restarts cleanly. Because the reset now clears status back to "playing" (plus score/history) and picks a new secret in the difficulty's range, the game actually restarts instead of being stuck on "You already won."

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

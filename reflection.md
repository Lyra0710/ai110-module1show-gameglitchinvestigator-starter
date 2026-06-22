# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
I used the developer debug info to see the number to be guessed and entered it to test. It worked successfully. 
- List at least two concrete bugs you noticed at the start  
1. Attempt counting is off by 1
2. Higher and lower are mixed up
3. New game does not work. Hardcoded range between 1-100 and not based on user chosen difficulty level. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|30 |Go HIGHER! | Go LOWER! |none |
|abc| Invalid Input, Attempts remain the same| Attempts down by 1 |None|
| New game| New game session| 'You already won. Start a new game to play again. |None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  I primarily used Chat GPT and Claude. 
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  While fixing the 'New Game' button issue, I did not realise that the range of the secret is hardcoded between 1-100. Claude removed that and added logic to use 'low' and 'high' instead. Upon prompting to explain, it explained that this is where the bug is for the difficulty level as well and it fixed it. 
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  When I asked Claude to fix the hint issue, it first suggested to remove the checks for the invalid inputs and also removed the lines that checked if the guess is the secret number.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I tested it by running app.py and verifying by using that specific feature. 
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
   I wrote a pytest file (test/test_game_logic.py) and ran it with pytest, which collected and passed 17 tests across the three bugs. The most useful one was for the higher/lower hint: check_guess(60, 50) should return the outcome "Too High" and a message telling the player to go LOWER, so I asserted that the message contains "LOWER" and does not contain "HIGHER". This showed me that checking the outcome label alone wasn't enough. The real bug was in the message text direction, so the test had to assert on the actual hint wording to be meaningful. I also tested the attempt-counting fix indirectly by checking that parse_guess("abc") returns ok=False, which is the gate that stops an invalid guess from spending an attempt. Running these confirmed the fixes held and gave me a regression check, since re-breaking a hint message makes the matching test fail immediately.
- Did AI help you design or understand any tests? How?
  Yes. Claude designed the pytest cases and explained the reasoning behind them. The most helpful insight was that for the higher/lower bug, asserting only on the outcome label ("Too High") wasn't enough. The actual bug was in the hint wording, so the test had to assert that the message says "LOWER" and not "HIGHER". It also pointed out that the attempt-counting fix lives in the app flow rather than a single function, so we tested the gate instead: that parse_guess returns ok=False for invalid input, which is what prevents an attempt from being spent. To make the "New Game" reset testable at all, it suggested pulling the reset logic into a new_game_state() function in logic_utils.py, since importing the whole Streamlit app into a test is messy.


---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  In Streamlit, every time you interact with the page, click a button, type in a box, change the difficulty, the entire app.py script reruns from top to bottom. That means normal variables get recreated from scratch each time, so they can't remember anything between clicks. Session state (st.session_state) is Streamlit's way to hold onto values across those reruns. It's where this game stores the secret number, attempts, score, status, and history so they survive each rerun. I really saw this with the "New Game" bug: clicking the button reset some session state but left status as "won", and because the script reran from the top, that stale value immediately stopped the game. The lesson was that anything that needs to persist must live in session state, and it has to be reset deliberately, because a rerun alone won't clear it.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  In this project, I learnt how to perform AI-assisted debugging, as compared to AI-driven debugging. It helped me verify the changes before implementing them, and this is a good practice to have for future projects. 
  
- What is one thing you would do differently next time you work with AI on a coding task?
  I would start by explaining the project instead of just dumping the files for AI to go over. I noticed that giving it more context increases it's accuracy of understanding the problem and implementing the solution you are looking for. 
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  The code generated by AI depends solely on how it understands the overall file, and it's relation to other files. Sometimes, it can misinterpret or hallucinate if the prompt given is not specific enough. Prompt engineering plays a big role in AI generated code. Furthermore, I realised that it takes longer to debug AI-driven code as compared to AI-assisted code. Human in the loop is a good approach to ensure accuracy. 

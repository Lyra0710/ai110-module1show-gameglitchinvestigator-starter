# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
I used the developer debug info to see the number to be guessed and entered it to test. It worked successfully. 
- List at least two concrete bugs you noticed at the start  
1. Attempt counting is off by 1
2. Higher and lower are mixed up
3. Hard range is 1 to 50, but the game still plays 1 to 100. Same with easy. 
4. New game does not work. 

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
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
1. When I asked Claude to fix the hint issue, it first suggested to remove the checks for the invalid inputs and also removed the lines that checked if the guess is the secret number.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

"""
PROJECT 01: NUMBER GUESSING GAME
==================================
The computer picks a random number. You try to guess it.

WHAT YOU'LL LEARN:
- if/elif/else — making decisions
- Comparison operators: ==, !=, <, >, <=, >=
- while loops — repeating until something happens
- The random module — generating random numbers
- break — escaping out of a loop

NEW CONCEPT — IMPORTING MODULES:
Python has tons of built-in tools. To use them, you "import" them.
Think of it like grabbing a specific toolbox from a shelf.
"""

# This gives us access to random number functions
import random

# ============================================================
# LESSON: if / elif / else
# ============================================================

# "if" checks a condition. If it's True, the indented code runs.
# "elif" (else if) checks another condition if the first was False.
# "else" runs if NOTHING above was True.

age = 20

if age < 13:
    print("You're a child.")
elif age < 18:
    print("You're a teenager.")
elif age < 65:
    print("You're an adult.")
else:
    print("You're a senior.")

# IMPORTANT: Notice the INDENTATION (the spaces before print).
# Python uses indentation to know what's "inside" the if block.
# Always use 4 spaces. Your editor should do this when you press Tab.

# ============================================================
# LESSON: Comparison operators
# ============================================================

# ==  equals (TWO equal signs! One = is for assigning variables)
# !=  not equal
# <   less than
# >   greater than
# <=  less than or equal
# >=  greater than or equal

print(5 == 5)    # True
print(5 != 3)    # True
print(5 > 10)    # False
print(5 <= 5)    # True

# ============================================================
# LESSON: while loops
# ============================================================

# A while loop keeps running AS LONG AS the condition is True.
# WARNING: If the condition is ALWAYS True, it loops forever!

count = 1
while count <= 5:
    print(f"Count is: {count}")
    count = count + 1  # Same as: count += 1
# After the loop, count is 6, so count <= 5 is False, and the loop stops.

# "break" immediately exits the loop:
# while True:
#     answer = input("Type 'quit' to exit: ")
#     if answer == "quit":
#         break  # ← Jumps out of the loop

# ============================================================
# THE PROJECT: Number Guessing Game
# ============================================================

print("\n=== NUMBER GUESSING GAME ===\n")

# random.randint(a, b) gives a random integer between a and b (inclusive)
secret_number = random.randint(1, 100)
attempts = 0
max_attempts = 7

print("I'm thinking of a number between 1 and 100.")
print(f"You have {max_attempts} attempts. Good luck!\n")

while attempts < max_attempts:
    # Get the player's guess
    guess = int(input(f"Attempt {attempts + 1}/{max_attempts} — Your guess: "))
    attempts += 1  # Same as: attempts = attempts + 1

    # Check the guess
    if guess == secret_number:
        print(f"\n🎉 CORRECT! The number was {secret_number}!")
        print(f"You got it in {attempts} attempt(s)!")
        break  # Exit the loop — they won!
    elif guess < secret_number:
        print("Too LOW! Guess higher.")
    else:
        print("Too HIGH! Guess lower.")

    # Show remaining attempts
    remaining = max_attempts - attempts
    if remaining > 0:
        print(f"({remaining} attempts left)\n")

# This runs AFTER the loop ends.
# If they used all attempts without guessing, they lost.
if guess != secret_number:
    print(f"\nGame over! The number was {secret_number}. Better luck next time!")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add difficulty levels.
# Easy: 1–50 with 10 guesses
# Medium: 1–100 with 7 guesses
# Hard: 1–500 with 10 guesses
# Ask the player which difficulty they want.
# YOUR CODE HERE:


# CHALLENGE 2: After the game ends, ask "Play again? (yes/no)".
# If yes, start a new game with a new random number.
# YOUR CODE HERE:


# CHALLENGE 3: Keep track of the player's best score (fewest guesses)
# across multiple games and show it at the end.
# YOUR CODE HERE:


# ============================================================
# DONE? Move on to 02_rock_paper_scissors.py!
# ============================================================

"""
PROJECT 07: HANGMAN
=====================
The classic word guessing game. Your biggest project yet!

WHAT YOU'LL LEARN:
- Combining loops, conditions, functions, and strings
- Lists (more practice)
- Tracking game state with multiple variables
- Building a bigger program step by step
"""

import random

# ============================================================
# THE PROJECT: Hangman
# ============================================================

# Word bank — the computer will pick one at random
WORDS = [
    "python", "javascript", "programming", "computer", "algorithm",
    "function", "variable", "keyboard", "internet", "database",
    "software", "developer", "terminal", "debug", "compile"
]

HANGMAN_STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    --------
    GAME OVER!
    """
]


def display_word(word, guessed_letters):
    """Show the word with unguessed letters as underscores."""
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()


def play_hangman():
    """Play one round of hangman."""
    word = random.choice(WORDS)
    guessed_letters = []
    wrong_guesses = 0
    max_wrong = len(HANGMAN_STAGES) - 1  # 6 wrong guesses allowed

    print("\n=== HANGMAN ===\n")
    print(f"The word has {len(word)} letters. You get {max_wrong} wrong guesses.")

    while wrong_guesses < max_wrong:
        # Show current state
        print(HANGMAN_STAGES[wrong_guesses])
        print(f"  Word: {display_word(word, guessed_letters)}")
        print(f"  Guessed: {', '.join(sorted(guessed_letters)) if guessed_letters else 'none'}")
        print(f"  Wrong guesses left: {max_wrong - wrong_guesses}")

        # Get a guess
        guess = input("\n  Guess a letter: ").lower().strip()

        # Validate the guess
        if len(guess) != 1 or not guess.isalpha():
            print("  Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print(f"  You already guessed '{guess}'. Try another letter.")
            continue

        guessed_letters.append(guess)

        # Check if the guess is in the word
        if guess in word:
            print(f"  YES! '{guess}' is in the word!")

            # Check if they've won (all letters guessed)
            all_guessed = True
            for letter in word:
                if letter not in guessed_letters:
                    all_guessed = False
                    break

            if all_guessed:
                print(f"\n  The word was: {word}")
                print("  YOU WIN! Congratulations!")
                return True  # Return True for a win
        else:
            wrong_guesses += 1
            print(f"  Nope! '{guess}' is not in the word.")

    # If we get here, they lost
    print(HANGMAN_STAGES[wrong_guesses])
    print(f"\n  The word was: {word}")
    print("  Better luck next time!")
    return False  # Return False for a loss


# --- Main program ---
wins = 0
total = 0

while True:
    won = play_hangman()
    total += 1
    if won:
        wins += 1

    print(f"\n  Record: {wins} wins out of {total} games")
    again = input("\n  Play again? (yes/no): ").lower().strip()
    if again != "yes" and again != "y":
        break

print("\nThanks for playing Hangman!")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add categories (animals, countries, foods).
# Let the player pick a category before the game starts.

# CHALLENGE 2: Add a hint system. The player can type "hint" to reveal
# one letter, but it costs them one wrong guess.

# CHALLENGE 3: Let two players play — one types the word (hidden),
# the other guesses it.


# ============================================================
# DONE? Move on to 08_adventure_game.py!
# ============================================================

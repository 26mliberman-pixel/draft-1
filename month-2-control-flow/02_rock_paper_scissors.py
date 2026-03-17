"""
PROJECT 02: ROCK PAPER SCISSORS
=================================
Play rock-paper-scissors against the computer.

WHAT YOU'LL LEARN:
- Logical operators: and, or, not
- random.choice() — picking from a list
- Lists (sneak peek!)
- Structuring a game loop
"""

import random

# ============================================================
# LESSON: Logical operators
# ============================================================

# "and" — Both must be True
# "or"  — At least one must be True
# "not" — Flips True to False and vice versa

age = 20
has_id = True

if age >= 18 and has_id:
    print("You may enter.")

if age < 13 or age > 65:
    print("You get a discount!")

if not has_id:
    print("No ID? No entry!")

# ============================================================
# LESSON: Lists (quick preview — full coverage in Month 3)
# ============================================================

# A list holds multiple values in order. Uses square brackets.
choices = ["rock", "paper", "scissors"]

# random.choice() picks one random item from a list
computer_pick = random.choice(choices)

# ============================================================
# THE PROJECT: Rock Paper Scissors
# ============================================================

print("=== ROCK PAPER SCISSORS ===\n")

wins = 0
losses = 0
ties = 0

while True:
    print("-" * 30)
    player = input("Choose rock, paper, or scissors (or 'quit'): ").lower().strip()

    if player == "quit":
        break

    if player not in ["rock", "paper", "scissors"]:
        print("Invalid choice! Try again.")
        continue  # Skip the rest of this loop iteration and go back to the top

    computer = random.choice(["rock", "paper", "scissors"])
    print(f"Computer chose: {computer}")

    # Determine the winner
    if player == computer:
        print("It's a TIE!")
        ties += 1
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        print("You WIN!")
        wins += 1
    else:
        print("You LOSE!")
        losses += 1

    print(f"Score → Wins: {wins} | Losses: {losses} | Ties: {ties}")

# Game over — show final score
print(f"\n=== FINAL SCORE ===")
print(f"Wins: {wins} | Losses: {losses} | Ties: {ties}")
total = wins + losses + ties
if total > 0:
    print(f"Win rate: {round(wins / total * 100, 1)}%")
print("Thanks for playing!")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add "lizard" and "Spock" (from Big Bang Theory).
# Scissors cuts Paper, Paper covers Rock, Rock crushes Lizard,
# Lizard poisons Spock, Spock smashes Scissors, Scissors decapitates Lizard,
# Lizard eats Paper, Paper disproves Spock, Spock vaporizes Rock,
# Rock crushes Scissors.

# CHALLENGE 2: Make it "best of 5" — first to 3 wins takes the match.

# CHALLENGE 3: Add a "computer personality" — the computer tends to favor
# one choice (e.g., picks rock 50% of the time). Let the player figure it out.


# ============================================================
# DONE? Move on to 03_countdown_timer.py!
# ============================================================

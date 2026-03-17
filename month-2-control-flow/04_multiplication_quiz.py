"""
PROJECT 04: MULTIPLICATION QUIZ
==================================
A timed math quiz with scoring.

WHAT YOU'LL LEARN:
- for loops and range()
- Keeping score with variables
- time module for measuring elapsed time
"""

import random
import time

# ============================================================
# LESSON: for loops and range()
# ============================================================

# A "for" loop goes through each item in a sequence.

# range(5) gives you: 0, 1, 2, 3, 4
for i in range(5):
    print(f"i is {i}")

# range(1, 6) gives you: 1, 2, 3, 4, 5
for i in range(1, 6):
    print(f"i is {i}")

# range(0, 10, 2) gives you: 0, 2, 4, 6, 8 (step by 2)
for i in range(0, 10, 2):
    print(f"i is {i}")

# You can loop through strings too:
for letter in "Hello":
    print(letter)

# ============================================================
# THE PROJECT: Multiplication Quiz
# ============================================================

print("=== MULTIPLICATION QUIZ ===\n")

num_questions = 10
score = 0
wrong_answers = []  # We'll store missed questions here (lists — Month 3!)

print(f"Answer {num_questions} multiplication questions as fast as you can!\n")

start_time = time.time()  # Record the start time

for question_num in range(1, num_questions + 1):
    # Generate two random numbers
    a = random.randint(2, 12)
    b = random.randint(2, 12)
    correct_answer = a * b

    # Ask the question
    user_answer = input(f"Q{question_num}: {a} × {b} = ")

    # Check if it's a number
    if user_answer.isdigit():
        if int(user_answer) == correct_answer:
            print("  ✓ Correct!\n")
            score += 1
        else:
            print(f"  ✗ Wrong! The answer was {correct_answer}.\n")
            wrong_answers.append(f"{a} × {b} = {correct_answer}")
    else:
        print(f"  ✗ That's not a number! The answer was {correct_answer}.\n")
        wrong_answers.append(f"{a} × {b} = {correct_answer}")

end_time = time.time()
elapsed = round(end_time - start_time, 1)

# Show results
print("=" * 30)
print(f"Score: {score}/{num_questions}")
print(f"Time:  {elapsed} seconds")
print(f"Avg:   {round(elapsed / num_questions, 1)} sec per question")

percentage = round(score / num_questions * 100)
if percentage == 100:
    print("PERFECT SCORE! Amazing!")
elif percentage >= 80:
    print("Great job!")
elif percentage >= 60:
    print("Not bad! Keep practicing.")
else:
    print("Keep studying those times tables!")

if wrong_answers:
    print(f"\nQuestions you missed:")
    for q in wrong_answers:
        print(f"  {q}")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Let the user choose difficulty:
# Easy: numbers 2–5, Medium: 2–10, Hard: 2–12

# CHALLENGE 2: Add different operations (addition, subtraction, division).
# Ask the user which type of quiz they want.

# CHALLENGE 3: Track a "streak" — how many correct in a row.
# Show the highest streak at the end.


# ============================================================
# DONE? Move on to 05_password_generator.py!
# ============================================================

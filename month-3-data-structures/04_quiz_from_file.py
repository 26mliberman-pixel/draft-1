"""
PROJECT 04: QUIZ GAME FROM FILE
==================================
A quiz game that loads questions from a file.

WHAT YOU'LL LEARN:
- Reading structured data from files
- Parsing text into useful data structures
- Separating data from code (good practice!)
"""

# ============================================================
# Step 1: Create a quiz file
# ============================================================

quiz_data = """What is the capital of France?|Paris|London|Berlin|Madrid|1
What does CPU stand for?|Central Processing Unit|Computer Personal Unit|Central Personal Utility|Core Processing Unit|1
Which planet is known as the Red Planet?|Jupiter|Mars|Venus|Saturn|2
What year did the first iPhone come out?|2005|2006|2007|2008|3
How many bits are in a byte?|4|6|8|16|3
What does HTML stand for?|Hyper Text Markup Language|High Tech Modern Language|Hyper Transfer Markup Language|Home Tool Markup Language|1
Which animal is the largest mammal?|Elephant|Blue Whale|Giraffe|Hippopotamus|2
What is the boiling point of water in Celsius?|90|95|100|110|3"""

# Create the quiz file
with open("quiz_questions.txt", "w") as f:
    f.write(quiz_data)

print("Created quiz_questions.txt!\n")

# ============================================================
# Step 2: Read and parse the quiz file
# ============================================================

def load_questions(filename):
    """Load questions from file and return as a list of dictionaries."""
    questions = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:  # Skip empty lines
                continue

            # Split the line by | character
            parts = line.split("|")

            # parts[0] = question
            # parts[1-4] = four answer choices
            # parts[5] = correct answer number (1-4)

            question = {
                "question": parts[0],
                "choices": [parts[1], parts[2], parts[3], parts[4]],
                "answer": int(parts[5])
            }
            questions.append(question)

    return questions


# ============================================================
# Step 3: Run the quiz
# ============================================================

import random

def run_quiz(questions):
    """Run the quiz and return the score."""
    random.shuffle(questions)  # Randomize order
    score = 0

    print(f"=== QUIZ TIME! ({len(questions)} questions) ===\n")

    for i, q in enumerate(questions, 1):
        print(f"Question {i}: {q['question']}")

        for j, choice in enumerate(q["choices"], 1):
            print(f"  {j}. {choice}")

        try:
            answer = int(input("\nYour answer (1-4): "))
        except ValueError:
            answer = 0

        if answer == q["answer"]:
            print("CORRECT!\n")
            score += 1
        else:
            correct = q["choices"][q["answer"] - 1]
            print(f"WRONG! The answer was: {correct}\n")

    return score


# --- Main program ---
questions = load_questions("quiz_questions.txt")
score = run_quiz(questions)

print(f"=== RESULTS ===")
print(f"Score: {score}/{len(questions)}")
percentage = round(score / len(questions) * 100)
print(f"Percentage: {percentage}%")

if percentage == 100:
    print("PERFECT!")
elif percentage >= 70:
    print("Great job!")
elif percentage >= 50:
    print("Not bad!")
else:
    print("Keep studying!")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add your own questions to the quiz file (at least 10 more).

# CHALLENGE 2: Add a "category" field to each question.
# Let the user choose which category to quiz on.

# CHALLENGE 3: Save high scores to a file. Show a leaderboard.

# CHALLENGE 4: Add a "review" mode at the end that shows only
# the questions you got wrong, with the correct answers.

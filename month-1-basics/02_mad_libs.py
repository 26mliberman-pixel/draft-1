"""
PROJECT 02: MAD LIBS
=====================
A fill-in-the-blank word game that teaches you about VARIABLES.

WHAT YOU'LL LEARN:
- Variables: storing data in named containers
- input(): asking the user to type something
- f-strings: mixing variables into text

NEW CONCEPTS:
- A VARIABLE is like a labeled box. You put something in it and use it later.
- variable_name = value     ← this is how you create a variable
- input("prompt")           ← asks the user for input and gives you back what they typed
"""

# ============================================================
# LESSON: Variables
# ============================================================

# Creating variables — think of these as labeled boxes.
name = "Alice"        # A string (text) variable
age = 25              # An integer (whole number) variable
height = 5.6          # A float (decimal number) variable

# Printing variables:
print(name)           # Prints: Alice
print(age)            # Prints: 25

# You can change what's in the box anytime:
name = "Bob"
print(name)           # Now prints: Bob

# ============================================================
# LESSON: input() — Getting info from the user
# ============================================================

# input() pauses the program and waits for the user to type something.
# Whatever they type becomes a STRING (text).

# Uncomment the lines below (remove the #) to try them:
# user_name = input("What is your name? ")
# print("Hello", user_name)

# ============================================================
# LESSON: f-strings — Mixing variables into text
# ============================================================

# f-strings start with f before the quotes.
# Put variable names inside curly braces {}.
animal = "cat"
color = "orange"
print(f"I have a {color} {animal}.")  # Prints: I have a orange cat.

# Without f-strings, you'd have to do this (uglier):
print("I have a " + color + " " + animal + ".")

# f-strings are way easier. Use them.

# ============================================================
# THE PROJECT: Build a Mad Libs game!
# ============================================================

print("=== MAD LIBS GAME ===")
print("I'm going to ask you for some words, then tell you a story!\n")

# Step 1: Ask the user for words
adjective1 = input("Give me an adjective (like 'big' or 'scary'): ")
noun1 = input("Give me a noun (like 'dog' or 'pizza'): ")
verb1 = input("Give me a verb (like 'run' or 'dance'): ")
place = input("Give me a place (like 'the moon' or 'Walmart'): ")
adjective2 = input("Give me another adjective: ")
noun2 = input("Give me another noun: ")

# Step 2: Print the story using f-strings
print("\n=== YOUR STORY ===\n")
print(f"Once upon a time, there was a {adjective1} {noun1}.")
print(f"Every day, it would {verb1} all the way to {place}.")
print(f"One day, it found a {adjective2} {noun2} on the ground.")
print(f"The {noun1} picked up the {noun2} and lived happily ever after.")
print("\n=== THE END ===")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add MORE words to the mad libs (a name, a number, a food, etc.)
# and make the story longer and funnier.

# CHALLENGE 2: Create a COMPLETELY DIFFERENT mad libs story.
# Ideas: a news report, a recipe, a love letter, a job application.

# CHALLENGE 3: Create variables for your personal info (name, age, hobby, etc.)
# and use f-strings to print a paragraph about yourself.
# Example output: "My name is Alice. I am 25 years old. I love painting."


# ============================================================
# DONE? Move on to 03_calculator.py!
# ============================================================

"""
PROJECT 01: HELLO WORLD
========================
Your very first program. Every programmer starts here.

WHAT YOU'LL LEARN:
- How to use print() to display text
- What strings are (text in quotes)
- How to run a Python file

HOW TO RUN THIS:
1. Open your terminal
2. Navigate to this folder: cd month-1-basics
3. Type: python 01_hello_world.py
4. Press Enter

INSTRUCTIONS:
Read through the code below. Run it. Then do the challenges at the bottom.
"""

# ============================================================
# LESSON: The print() function
# ============================================================

# This is a comment. Python ignores everything after the # symbol.
# Comments are notes for humans, not for the computer.

# print() displays text on the screen. The text goes inside quotes.
print("Hello, World!")

# You can use single quotes OR double quotes — both work.
print('Hello again!')

# You can print numbers without quotes.
print(42)
print(3.14)

# You can print multiple things separated by commas.
# Python will put a space between them automatically.
print("My favorite number is", 7)

# You can print blank lines to add spacing.
print()  # This prints an empty line
print("There was a blank line above me.")

# ============================================================
# LESSON: Escape characters
# ============================================================

# What if you want a quote inside your string?
# Use the OTHER type of quote on the outside:
print("It's a beautiful day!")
print('She said "hello" to me.')

# \n creates a new line INSIDE a string:
print("Line one\nLine two\nLine three")

# \t creates a tab (big space):
print("Name:\tAlice")
print("Age:\t25")

# ============================================================
# YOUR TURN — CHALLENGES
# ============================================================

# CHALLENGE 1: Print your name.
# Example: print("Alice")
# YOUR CODE HERE:


# CHALLENGE 2: Print your age on one line, and your city on the next line,
# using a SINGLE print statement and \n.
# YOUR CODE HERE:


# CHALLENGE 3: Print this exact text (including the quotes):
# She said "Python is awesome!"
# YOUR CODE HERE:


# CHALLENGE 4: Print a little ASCII art. Here's an example, but make your own:
#   /\_/\
#  ( o.o )
#   > ^ <
# Hint: You'll need multiple print statements.
# YOUR CODE HERE:


# ============================================================
# DONE? Move on to 02_mad_libs.py!
# ============================================================

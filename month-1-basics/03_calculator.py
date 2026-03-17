"""
PROJECT 03: BASIC CALCULATOR
==============================
A calculator that does math with numbers the user types in.

WHAT YOU'LL LEARN:
- Math operators: +, -, *, /, //, %, **
- Type conversion: turning strings into numbers with int() and float()
- Why input() always gives you a string, even if you type a number

KEY CONCEPT:
When you type "5" using input(), Python sees the TEXT "5", not the NUMBER 5.
"5" + "3" = "53" (text joined together)
 5  +  3  = 8   (actual math)
You must CONVERT the text to a number first using int() or float().
"""

# ============================================================
# LESSON: Math operators
# ============================================================

print("=== MATH IN PYTHON ===\n")

# Basic math — just like a calculator:
print("10 + 3 =", 10 + 3)    # Addition → 13
print("10 - 3 =", 10 - 3)    # Subtraction → 7
print("10 * 3 =", 10 * 3)    # Multiplication → 30
print("10 / 3 =", 10 / 3)    # Division → 3.3333... (always gives a float!)

# These two are new:
print("10 // 3 =", 10 // 3)  # Floor division → 3 (chops off the decimal)
print("10 % 3 =", 10 % 3)    # Modulo → 1 (the REMAINDER after division)
print("10 ** 3 =", 10 ** 3)  # Exponent → 1000 (10 to the power of 3)

# ============================================================
# LESSON: Type conversion (VERY IMPORTANT)
# ============================================================

print("\n=== TYPE CONVERSION ===\n")

# This is a STRING (text), even though it looks like a number:
number_text = "42"
print(type(number_text))  # Shows: <class 'str'>

# Convert string to integer:
number_int = int("42")
print(type(number_int))   # Shows: <class 'int'>

# Convert string to float (decimal):
number_float = float("3.14")
print(type(number_float)) # Shows: <class 'float'>

# THE COMMON BEGINNER MISTAKE:
# name = input("Enter a number: ")  ← This gives you a STRING!
# name + 5  ← ERROR! Can't add text and a number!
# int(name) + 5  ← This works! Convert it first.

# ============================================================
# THE PROJECT: Build a calculator
# ============================================================

print("\n=== CALCULATOR ===\n")

# Get two numbers from the user.
# IMPORTANT: We wrap input() with float() to convert text → number.
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

# Do all the math:
print(f"\n--- Results ---")
print(f"{num1} + {num2} = {num1 + num2}")
print(f"{num1} - {num2} = {num1 - num2}")
print(f"{num1} * {num2} = {num1 * num2}")
print(f"{num1} / {num2} = {num1 / num2}")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add floor division (//), modulo (%), and exponent (**)
# to the results above.

# CHALLENGE 2: Ask the user which operation they want to perform
# (e.g., "Do you want to add, subtract, multiply, or divide?")
# and only show THAT result.
# Hint: You'll need if/else from next month, but try it anyway!

# CHALLENGE 3: Calculate the average of THREE numbers.
# Ask the user for 3 numbers, add them up, divide by 3, print the result.
# YOUR CODE HERE:


# CHALLENGE 4: Build a "percentage calculator."
# Ask: "What is X% of Y?"
# Example: "What is 15% of 200?" → Answer: 30
# Formula: (X / 100) * Y
# YOUR CODE HERE:


# ============================================================
# DONE? Move on to 04_temperature_converter.py!
# ============================================================

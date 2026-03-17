"""
PROJECT 05: PASSWORD GENERATOR
=================================
Generate random secure passwords. THIS is where you learn functions.

WHAT YOU'LL LEARN:
- Defining and calling functions
- Parameters and return values
- The string module
- Default parameters

FUNCTIONS ARE THE #1 MOST IMPORTANT CONCEPT IN PROGRAMMING.
A function is a reusable block of code with a name. Instead of writing
the same code over and over, you write it once as a function and call it
whenever you need it.
"""

import random
import string

# ============================================================
# LESSON: Functions
# ============================================================

# This is how you DEFINE a function:
def say_hello():
    print("Hello!")

# This is how you CALL (use) a function:
say_hello()  # Prints: Hello!
say_hello()  # You can call it as many times as you want!

# ============================================================
# LESSON: Parameters — Giving data TO a function
# ============================================================

def greet(name):
    print(f"Hello, {name}!")

greet("Alice")   # Prints: Hello, Alice!
greet("Bob")     # Prints: Hello, Bob!

# Multiple parameters:
def add(a, b):
    print(f"{a} + {b} = {a + b}")

add(3, 5)   # Prints: 3 + 5 = 8
add(10, 20) # Prints: 10 + 20 = 30

# ============================================================
# LESSON: Return values — Getting data BACK from a function
# ============================================================

# "return" sends a value back to wherever the function was called.

def multiply(a, b):
    return a * b    # Gives back the result

result = multiply(4, 5)  # result is now 20
print(result)

# Without return, the function gives back None (nothing):
def no_return(a, b):
    a + b  # Does the math but doesn't return it!

result = no_return(4, 5)
print(result)  # None

# ============================================================
# LESSON: Default parameters
# ============================================================

def greet_fancy(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet_fancy("Alice")             # Uses default: "Hello, Alice!"
greet_fancy("Alice", "Howdy")    # Uses custom: "Howdy, Alice!"

# ============================================================
# LESSON: The string module
# ============================================================

# string.ascii_lowercase = "abcdefghijklmnopqrstuvwxyz"
# string.ascii_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# string.digits = "0123456789"
# string.punctuation = "!@#$%^&*()..."

print(string.ascii_lowercase)
print(string.digits)
print(string.punctuation)

# ============================================================
# THE PROJECT: Password Generator
# ============================================================

def generate_password(length=12, use_uppercase=True, use_numbers=True, use_symbols=True):
    """Generate a random password with the given settings."""
    # Start with lowercase letters (always included)
    characters = string.ascii_lowercase

    # Add character types based on settings
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    # Build the password by picking random characters
    password = ""
    for i in range(length):
        password += random.choice(characters)

    return password


def check_password_strength(password):
    """Check how strong a password is."""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Too short (need 8+ characters)")

    if len(password) >= 12:
        score += 1

    has_upper = False
    has_lower = False
    has_digit = False
    has_symbol = False

    for char in password:
        if char in string.ascii_uppercase:
            has_upper = True
        elif char in string.ascii_lowercase:
            has_lower = True
        elif char in string.digits:
            has_digit = True
        elif char in string.punctuation:
            has_symbol = True

    if has_upper:
        score += 1
    else:
        feedback.append("Add uppercase letters")
    if has_lower:
        score += 1
    else:
        feedback.append("Add lowercase letters")
    if has_digit:
        score += 1
    else:
        feedback.append("Add numbers")
    if has_symbol:
        score += 1
    else:
        feedback.append("Add symbols")

    # Rate the password
    if score <= 2:
        strength = "WEAK"
    elif score <= 4:
        strength = "MEDIUM"
    else:
        strength = "STRONG"

    return strength, feedback  # You can return multiple values!


# --- Main program ---
print("=== PASSWORD GENERATOR ===\n")

while True:
    print("Options:")
    print("  1. Generate a password")
    print("  2. Check a password's strength")
    print("  3. Quit")

    choice = input("\nPick an option (1/2/3): ")

    if choice == "1":
        length = int(input("Password length (default 12): ") or "12")
        password = generate_password(length)
        print(f"\nYour password: {password}")
        strength, _ = check_password_strength(password)
        print(f"Strength: {strength}\n")

    elif choice == "2":
        password = input("Enter a password to check: ")
        strength, feedback = check_password_strength(password)
        print(f"\nStrength: {strength}")
        if feedback:
            print("Suggestions:")
            for tip in feedback:
                print(f"  - {tip}")
        print()

    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid option. Try again.\n")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a "memorable password" option that generates
# passwords like "correct-horse-battery-staple" (random words joined
# by dashes). Hint: create a list of common words.

# CHALLENGE 2: Generate MULTIPLE passwords at once and let the user pick.

# CHALLENGE 3: Add a "no ambiguous characters" option that removes
# characters like 0/O, 1/l/I that look similar.


# ============================================================
# DONE? Move on to 06_simple_atm.py!
# ============================================================

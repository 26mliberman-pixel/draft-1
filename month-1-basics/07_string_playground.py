"""
PROJECT 07: STRING PLAYGROUND
================================
Learn all the ways you can manipulate text in Python.

WHAT YOU'LL LEARN:
- String methods: upper(), lower(), strip(), replace(), etc.
- String indexing and slicing
- len() — how to measure the length of a string
- The "in" keyword

WHAT IS A "METHOD"?
A method is a function that belongs to something. Strings have built-in methods.
You call them with a dot: "hello".upper() → "HELLO"
"""

# ============================================================
# LESSON: String methods
# ============================================================

message = "  Hello, World!  "

# Changing case:
print(message.upper())       # "  HELLO, WORLD!  "
print(message.lower())       # "  hello, world!  "
print(message.title())       # "  Hello, World!  "

# Removing whitespace (spaces at the edges):
print(message.strip())       # "Hello, World!" (both sides trimmed)
print(message.lstrip())      # "Hello, World!  " (left side trimmed)
print(message.rstrip())      # "  Hello, World!" (right side trimmed)

# Replacing text:
print(message.replace("World", "Python"))  # "  Hello, Python!  "

# Counting and finding:
text = "banana"
print(text.count("a"))       # 3 (how many times "a" appears)
print(text.find("nan"))      # 2 (where "nan" starts — position 2)
print(text.find("xyz"))      # -1 (not found)

# Checking what's in a string:
print("ban" in "banana")     # True
print("xyz" in "banana")     # False

# Checking type of content:
print("hello".isalpha())     # True (only letters)
print("12345".isdigit())     # True (only numbers)
print("hello123".isalnum())  # True (letters or numbers)

# ============================================================
# LESSON: String indexing — Getting individual characters
# ============================================================

#        0123456789...
word = "P y t h o n"
# Index: 0 1 2 3 4 5

word = "Python"
print(word[0])   # P  (first character — counting starts at 0!)
print(word[1])   # y
print(word[-1])  # n  (last character)
print(word[-2])  # o  (second to last)

# ============================================================
# LESSON: String slicing — Getting pieces of strings
# ============================================================

# word[start:end]  — gets characters from "start" up to BUT NOT INCLUDING "end"
word = "Python"
print(word[0:3])  # "Pyt" (characters 0, 1, 2)
print(word[2:5])  # "tho" (characters 2, 3, 4)
print(word[:3])   # "Pyt" (from the beginning to 3)
print(word[3:])   # "hon" (from 3 to the end)
print(word[::-1]) # "nohtyP" (reversed!)

# ============================================================
# LESSON: len() — Measuring strings
# ============================================================

greeting = "Hello!"
print(len(greeting))   # 6 (counts every character, including !)

# ============================================================
# THE PROJECT: String Playground
# ============================================================

print("\n=== STRING PLAYGROUND ===\n")

user_text = input("Type any sentence: ")

print(f"\nHere's what I can do with your text:\n")
print(f"  UPPERCASE:    {user_text.upper()}")
print(f"  lowercase:    {user_text.lower()}")
print(f"  Title Case:   {user_text.title()}")
print(f"  Reversed:     {user_text[::-1]}")
print(f"  Length:        {len(user_text)} characters")
print(f"  Word count:   ~{len(user_text.split())} words")
print(f"  First char:   {user_text[0]}")
print(f"  Last char:    {user_text[-1]}")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Build a "password strength checker."
# - Check if the password is at least 8 characters (len)
# - Check if it has at least one number (loop through chars, use .isdigit())
# - Print "Weak", "Medium", or "Strong" based on your criteria.
# YOUR CODE HERE:


# CHALLENGE 2: Build a "text censor."
# Ask the user for a sentence and a word to censor.
# Replace that word with asterisks (****).
# Example: "I love pizza" censor "pizza" → "I love *****"
# Hint: Use .replace() and "*" * len(word)
# YOUR CODE HERE:


# CHALLENGE 3: Check if a word is a palindrome.
# A palindrome reads the same forwards and backwards (e.g., "racecar").
# Hint: Compare the word to its reverse (word[::-1])
# YOUR CODE HERE:


# ============================================================
# DONE? Move on to 08_personal_info_card.py!
# ============================================================

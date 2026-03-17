"""
PROJECT 08: PERSONAL INFO CARD
================================
Build a formatted profile card — your Month 1 capstone!

WHAT YOU'LL LEARN:
- Putting ALL Month 1 skills together
- String formatting and alignment
- Making output look nice

THIS PROJECT COMBINES:
- print() and f-strings (Project 01)
- Variables and input() (Project 02)
- Math operations (Project 03)
- Type conversion (Project 04)
- Number formatting (Project 05 & 06)
- String methods (Project 07)
"""

# ============================================================
# THE PROJECT: Personal Info Card Generator
# ============================================================

print("=== PERSONAL INFO CARD GENERATOR ===")
print("Answer the questions below and I'll make you a fancy card!\n")

# Gather information
first_name = input("First name: ")
last_name = input("Last name: ")
age = int(input("Age: "))
city = input("City: ")
country = input("Country: ")
hobby = input("Favorite hobby: ")
fav_food = input("Favorite food: ")
fav_color = input("Favorite color: ")
job = input("Job title (or 'Student'): ")

# Process the data
full_name = f"{first_name} {last_name}".title()  # Capitalize properly
initials = f"{first_name[0].upper()}.{last_name[0].upper()}."
name_length = len(full_name)
birth_year = 2026 - age
days_alive = age * 365

# Build the card
width = 50  # Width of the card

print("\n")
print("+" + "=" * width + "+")
print("|" + full_name.center(width) + "|")
print("|" + f"({initials})".center(width) + "|")
print("+" + "-" * width + "+")
print("|" + f"  Age:      {age} (born ~{birth_year})".ljust(width) + "|")
print("|" + f"  Location: {city}, {country}".ljust(width) + "|")
print("|" + f"  Job:      {job}".ljust(width) + "|")
print("+" + "-" * width + "+")
print("|" + f"  Hobby:    {hobby}".ljust(width) + "|")
print("|" + f"  Food:     {fav_food}".ljust(width) + "|")
print("|" + f"  Color:    {fav_color}".ljust(width) + "|")
print("+" + "-" * width + "+")
print("|" + f"  Days alive: ~{days_alive:,}".ljust(width) + "|")
print("|" + f"  Fun fact: Name has {name_length} characters!".ljust(width) + "|")
print("+" + "=" * width + "+")

# ============================================================
# LESSON: String alignment methods
# ============================================================

# .center(width) — centers text in a given width
# .ljust(width)  — left-justifies text
# .rjust(width)  — right-justifies text

# "Hi".center(10) → "    Hi    "
# "Hi".ljust(10)  → "Hi        "
# "Hi".rjust(10)  → "        Hi"

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add more fields to the card:
# - Email, phone number, or social media
# - A short bio (limit it to 50 characters using slicing)
# YOUR CODE HERE:


# CHALLENGE 2: Let the user choose a "card style":
# - Style 1: The box style above
# - Style 2: A simpler style with just dashes
# - Style 3: A fancy style with stars or other characters
# YOUR CODE HERE:


# CHALLENGE 3: Generate multiple cards!
# Ask "Do you want to create another card? (yes/no)"
# If yes, run the whole thing again.
# Hint: You'll need a while loop (sneak peek at Month 2!)
# YOUR CODE HERE:


# ============================================================
# CONGRATULATIONS! You've completed Month 1!
#
# You now know:
# ✓ How to print text to the screen
# ✓ How to store data in variables
# ✓ How to get input from users
# ✓ How to do math
# ✓ How to convert between data types
# ✓ How to format numbers and strings
# ✓ How to manipulate text with string methods
# ✓ How to index and slice strings
#
# Head over to month-2-control-flow/ to keep going!
# ============================================================

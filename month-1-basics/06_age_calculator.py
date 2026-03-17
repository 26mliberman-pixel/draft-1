"""
PROJECT 06: AGE CALCULATOR
============================
Calculate someone's age and fun facts about their life.

WHAT YOU'LL LEARN:
- More practice with math operations
- Using multiple calculations together
- Integer vs. float division
"""

# ============================================================
# THE PROJECT: Age Calculator
# ============================================================

print("=== AGE CALCULATOR ===\n")

name = input("What's your name? ")
birth_year = int(input("What year were you born? "))
current_year = 2026  # Update this if you're reading in the future!

# Basic age calculation
age = current_year - birth_year
print(f"\nHey {name}! You are (or will turn) {age} years old this year.\n")

# Fun facts
print("=== FUN FACTS ABOUT YOUR LIFE ===\n")

days_alive = age * 365
hours_alive = days_alive * 24
minutes_alive = hours_alive * 60
heartbeats = minutes_alive * 72  # Average resting heart rate

print(f"You've been alive for approximately:")
print(f"  {days_alive:,} days")         # :, adds commas (1000 → 1,000)
print(f"  {hours_alive:,} hours")
print(f"  {minutes_alive:,} minutes")
print(f"  {heartbeats:,} heartbeats")

print(f"\nIn dog years, you'd be {age * 7} years old.")
print(f"You've slept about {round(days_alive / 3):,} days (1/3 of your life!).")
print(f"You've eaten roughly {days_alive * 3:,} meals.")

# When will they turn 100?
year_100 = birth_year + 100
print(f"\nYou'll turn 100 in the year {year_100}!")

# ============================================================
# LESSON: The :, format specifier
# ============================================================

# f"{number:,}" adds commas to big numbers.
# 1000000 → "1,000,000"
# This makes big numbers WAY easier to read.

big_number = 7894561230
print(f"\n{big_number}")    # 7894561230 (hard to read)
print(f"{big_number:,}")    # 7,894,561,230 (easy to read!)

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Ask for their birth MONTH and DAY too.
# Calculate if they've already had their birthday this year.
# If not, subtract 1 from the age.
# YOUR CODE HERE:


# CHALLENGE 2: Calculate what year they'll be at various milestones:
# - When they can drive (16)
# - When they can vote (18)
# - When they can drink (21)
# - When they can retire (65)
# If they've already passed a milestone, say "Already passed!"
# YOUR CODE HERE:


# CHALLENGE 3: Ask for TWO people's birth years.
# Calculate who is older and by how many years.
# YOUR CODE HERE:


# ============================================================
# DONE? Move on to 07_string_playground.py!
# ============================================================

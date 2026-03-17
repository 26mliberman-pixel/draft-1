"""
PROJECT 05: TIP CALCULATOR
============================
Calculate the tip at a restaurant and split the bill.

WHAT YOU'LL LEARN:
- Combining everything from projects 01–04
- Formatting money (2 decimal places)
- Breaking a problem into steps

REAL-WORLD SKILL:
This is how programmers think — break a big problem into small steps:
1. Get the bill amount
2. Get the tip percentage
3. Get the number of people
4. Calculate
5. Display results
"""

# ============================================================
# THE PROJECT: Tip Calculator
# ============================================================

print("=== TIP CALCULATOR ===\n")

# Step 1: Get the info from the user
bill = float(input("What was the total bill? $"))
tip_percent = float(input("What tip percentage do you want to leave? (e.g., 15, 18, 20): "))
num_people = int(input("How many people are splitting the bill? "))

# Step 2: Do the math
tip_amount = bill * (tip_percent / 100)
total = bill + tip_amount
per_person = total / num_people

# Step 3: Display the results
# :.2f means "format as a float with 2 decimal places" (perfect for money!)
print(f"\n--- Bill Summary ---")
print(f"Bill:            ${bill:.2f}")
print(f"Tip ({tip_percent}%):     ${tip_amount:.2f}")
print(f"Total:           ${total:.2f}")
print(f"Per person ({num_people}):  ${per_person:.2f}")

# ============================================================
# LESSON: String formatting with :.2f
# ============================================================

# :.2f is a FORMAT SPECIFIER. It goes inside f-string curly braces.
#
# f"{number:.2f}"  → 2 decimal places   → "3.14"
# f"{number:.1f}"  → 1 decimal place    → "3.1"
# f"{number:.0f}"  → 0 decimal places   → "3"
# f"{number:>10}"  → right-align in 10 spaces
# f"{number:<10}"  → left-align in 10 spaces
#
# Example:
price = 9.99
print(f"\nThe price is ${price:.2f}")  # The price is $9.99

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Show three tip options (15%, 18%, 20%) and the cost
# for each, so the user can compare before deciding.
# YOUR CODE HERE:


# CHALLENGE 2: Add tax calculation. Ask for the tax rate (e.g., 8.5%)
# and calculate: bill + tax + tip = total.
# YOUR CODE HERE:


# CHALLENGE 3: Handle edge cases:
# - What if someone enters 0 people? (You'd divide by zero — crash!)
# - What if someone enters a negative bill?
# Print a helpful error message instead of crashing.
# YOUR CODE HERE:


# ============================================================
# DONE? Move on to 06_age_calculator.py!
# ============================================================

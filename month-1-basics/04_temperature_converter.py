"""
PROJECT 04: TEMPERATURE CONVERTER
===================================
Convert between Fahrenheit and Celsius.

WHAT YOU'LL LEARN:
- Using formulas in code
- Rounding numbers with round()
- Putting it all together: input → math → output

FORMULAS:
- Celsius to Fahrenheit: F = (C * 9/5) + 32
- Fahrenheit to Celsius: C = (F - 32) * 5/9
"""

# ============================================================
# LESSON: round() — Cleaning up decimal numbers
# ============================================================

ugly_number = 3.141592653589793
print(ugly_number)            # All the decimals
print(round(ugly_number, 2))  # Rounded to 2 decimal places → 3.14
print(round(ugly_number, 1))  # Rounded to 1 decimal place → 3.1
print(round(ugly_number))     # Rounded to nearest whole number → 3

# ============================================================
# THE PROJECT: Temperature Converter
# ============================================================

print("=== TEMPERATURE CONVERTER ===\n")

# Ask for the temperature
temp = float(input("Enter the temperature: "))
unit = input("Is that in (F)ahrenheit or (C)elsius? Type F or C: ")

# Convert based on what they chose
if unit == "C" or unit == "c":
    # Celsius to Fahrenheit
    result = (temp * 9/5) + 32
    print(f"\n{temp}°C = {round(result, 1)}°F")
elif unit == "F" or unit == "f":
    # Fahrenheit to Celsius
    result = (temp - 32) * 5/9
    print(f"\n{temp}°F = {round(result, 1)}°C")
else:
    print("I don't understand. Please type F or C next time.")

# ============================================================
# WAIT — what's "if" and "elif" and "else"?
# ============================================================

# We're getting a sneak peek at Month 2 here. Don't worry about it too much.
#
# if (something is true):
#     do this
# elif (something else is true):
#     do this instead
# else:
#     do this if nothing above was true
#
# You'll learn all about this in Month 2. For now, just notice the pattern.

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Also handle Kelvin conversions.
# Celsius to Kelvin: K = C + 273.15
# Kelvin to Celsius: C = K - 273.15
# YOUR CODE HERE:


# CHALLENGE 2: After converting, ask the user if they want to convert another
# temperature. If they say "yes", do it again.
# Hint: You'll need a "while" loop (Month 2), but try to figure it out!

# CHALLENGE 3: Print a mini conversion table:
# Show 0°C, 10°C, 20°C, 30°C, 40°C, 50°C and their Fahrenheit values.
# Just use multiple print() statements for now.
# YOUR CODE HERE:


# ============================================================
# DONE? Move on to 05_tip_calculator.py!
# ============================================================

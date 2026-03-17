"""
PROJECT 03: COUNTDOWN TIMER
==============================
A real working countdown timer.

WHAT YOU'LL LEARN:
- The time module (time.sleep)
- More while loop practice
- Breaking a problem into steps
"""

import time

# ============================================================
# LESSON: The time module
# ============================================================

# time.sleep(seconds) pauses the program for that many seconds.
print("Wait for it...")
time.sleep(1)  # Pause for 1 second
print("...there it is!")

# ============================================================
# THE PROJECT: Countdown Timer
# ============================================================

print("\n=== COUNTDOWN TIMER ===\n")

# Get time from user
minutes = int(input("Enter minutes: "))
seconds = int(input("Enter seconds: "))

# Convert everything to seconds
total_seconds = (minutes * 60) + seconds

print(f"\nTimer set for {minutes} min {seconds} sec. Starting...\n")

# The countdown loop
while total_seconds > 0:
    # Convert total seconds back to minutes:seconds for display
    mins = total_seconds // 60    # How many full minutes
    secs = total_seconds % 60     # Remaining seconds

    # :02d means "format as integer with at least 2 digits, pad with zeros"
    # So 5 becomes "05" and 12 stays "12"
    print(f"  {mins:02d}:{secs:02d}", end="\r")  # \r returns cursor to start of line
    # end="\r" makes it overwrite the same line (looks like a real timer!)

    time.sleep(1)        # Wait 1 second
    total_seconds -= 1   # Subtract 1

print("  00:00")
print("\n⏰ TIME'S UP!")

# Optional: make a "beep" sound
print("\a")  # This might make a beep sound on some systems

# ============================================================
# LESSON: end="\r" and end="" in print()
# ============================================================

# print() normally ends with a newline (\n) — it moves to the next line.
# You can change this with the "end" parameter:
#
# print("Hello", end="")    → No newline. Next print continues on same line.
# print("Hello", end="\r")  → Carriage return. Cursor goes to START of line.
# print("Hello", end=" ")   → Ends with a space instead of newline.

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a "pomodoro timer" mode:
# Work for 25 minutes, break for 5 minutes, repeat 4 times.
# Show which round you're on.

# CHALLENGE 2: Let the user set multiple timers in sequence.
# "Boil water: 3 minutes" → "Add pasta: 10 minutes" → "Done!"

# CHALLENGE 3: Add the ability to PAUSE the timer by pressing Enter.
# (This is tricky! Hint: use threading or just check for input.)


# ============================================================
# DONE? Move on to 04_multiplication_quiz.py!
# ============================================================

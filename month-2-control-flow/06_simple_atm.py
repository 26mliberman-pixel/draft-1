"""
PROJECT 06: SIMPLE ATM
========================
A simulated ATM machine — deposit, withdraw, check balance.

WHAT YOU'LL LEARN:
- Functions that modify state (using a global variable or passing values)
- try/except — handling errors gracefully
- Structuring a bigger program with multiple functions
- Input validation

NEW CONCEPT — try/except:
Sometimes users type garbage. Instead of crashing, we can CATCH the error
and handle it nicely.
"""

# ============================================================
# LESSON: try / except — Catching errors
# ============================================================

# WITHOUT try/except:
# number = int(input("Enter a number: "))
# If the user types "abc", Python CRASHES with a ValueError.

# WITH try/except:
try:
    number = int("abc")  # This will fail
except ValueError:
    print("That's not a valid number!")
# The program continues running — no crash!

# You can catch specific error types:
# ValueError — wrong type of value (e.g., int("abc"))
# ZeroDivisionError — dividing by zero
# FileNotFoundError — file doesn't exist
# Exception — catches ANY error (use as last resort)

# ============================================================
# THE PROJECT: Simple ATM
# ============================================================

# This variable tracks the balance across all functions
balance = 1000.00  # Starting balance


def show_balance():
    """Display the current balance."""
    print(f"\n  Current balance: ${balance:,.2f}\n")


def deposit():
    """Add money to the account."""
    global balance  # This lets us modify the variable defined outside the function

    try:
        amount = float(input("  How much do you want to deposit? $"))
    except ValueError:
        print("  Invalid amount. Please enter a number.")
        return

    if amount <= 0:
        print("  Deposit amount must be positive.")
        return

    balance += amount
    print(f"  Deposited ${amount:,.2f}")
    print(f"  New balance: ${balance:,.2f}")


def withdraw():
    """Take money out of the account."""
    global balance

    try:
        amount = float(input("  How much do you want to withdraw? $"))
    except ValueError:
        print("  Invalid amount. Please enter a number.")
        return

    if amount <= 0:
        print("  Withdrawal amount must be positive.")
        return

    if amount > balance:
        print(f"  Insufficient funds! Your balance is ${balance:,.2f}")
        return

    balance -= amount
    print(f"  Withdrew ${amount:,.2f}")
    print(f"  New balance: ${balance:,.2f}")


def transfer():
    """Simulate transferring money to someone."""
    global balance

    recipient = input("  Who do you want to send money to? ")
    try:
        amount = float(input(f"  How much to send to {recipient}? $"))
    except ValueError:
        print("  Invalid amount.")
        return

    if amount <= 0:
        print("  Amount must be positive.")
        return

    if amount > balance:
        print(f"  Insufficient funds! Your balance is ${balance:,.2f}")
        return

    balance -= amount
    print(f"\n  Sent ${amount:,.2f} to {recipient}.")
    print(f"  New balance: ${balance:,.2f}")


# --- Main program loop ---
print("=" * 40)
print("  Welcome to the Python ATM!")
print("=" * 40)

# Simple PIN check
correct_pin = "1234"
attempts = 3

while attempts > 0:
    pin = input("\nEnter your PIN: ")
    if pin == correct_pin:
        break
    attempts -= 1
    print(f"Wrong PIN. {attempts} attempts remaining.")

if attempts == 0:
    print("Too many failed attempts. Account locked.")
else:
    # Main menu loop
    while True:
        print("\n" + "-" * 30)
        print("  1. Check Balance")
        print("  2. Deposit")
        print("  3. Withdraw")
        print("  4. Transfer")
        print("  5. Exit")
        print("-" * 30)

        choice = input("Choose an option: ")

        if choice == "1":
            show_balance()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            transfer()
        elif choice == "5":
            print(f"\n  Final balance: ${balance:,.2f}")
            print("  Thank you for using Python ATM. Goodbye!\n")
            break
        else:
            print("  Invalid option. Please choose 1-5.")

# ============================================================
# LESSON: "global" keyword
# ============================================================

# When you modify a variable that was defined OUTSIDE a function,
# you need to say "global variable_name" inside the function.
# Otherwise, Python thinks you're creating a NEW local variable.
#
# This is considered a bit messy. In Month 4, you'll learn CLASSES,
# which are a cleaner way to handle this.

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a "transaction history" — store every transaction
# (type, amount, new balance) in a list and let the user view it.

# CHALLENGE 2: Add a daily withdrawal limit of $500.

# CHALLENGE 3: Add interest! Every time the user checks their balance,
# add 0.1% interest (balance * 0.001) and show it.


# ============================================================
# DONE? Move on to 07_hangman.py!
# ============================================================

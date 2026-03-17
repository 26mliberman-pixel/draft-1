"""
PROJECT 01: BANK ACCOUNT CLASS
=================================
Rebuild the ATM from Month 2, but now with CLASSES.

WHAT YOU'LL LEARN:
- Classes and objects
- __init__ (the constructor)
- self — referring to the current object
- Methods (functions that belong to a class)
- __str__ (how an object describes itself as text)

WHY CLASSES?
Remember how the ATM used "global" variables? That was messy.
Classes bundle DATA (the balance) and BEHAVIOR (deposit, withdraw)
together into one clean package.
"""

# ============================================================
# LESSON: Classes and Objects
# ============================================================

# A CLASS is a blueprint. An OBJECT is a thing made from that blueprint.
# Class = "Dog" (the concept)
# Object = "My specific dog named Max"

class Dog:
    def __init__(self, name, breed):
        # __init__ runs automatically when you create a new Dog
        # "self" refers to THIS specific dog
        self.name = name
        self.breed = breed
        self.tricks = []

    def learn_trick(self, trick):
        self.tricks.append(trick)

    def show_tricks(self):
        if self.tricks:
            print(f"{self.name} knows: {', '.join(self.tricks)}")
        else:
            print(f"{self.name} doesn't know any tricks yet.")

    def __str__(self):
        # This controls what happens when you print() the object
        return f"{self.name} the {self.breed}"


# Creating OBJECTS (instances) from the class:
dog1 = Dog("Max", "Golden Retriever")
dog2 = Dog("Luna", "Husky")

print(dog1)           # "Max the Golden Retriever" (uses __str__)
print(dog2.name)      # "Luna"

dog1.learn_trick("sit")
dog1.learn_trick("shake")
dog1.show_tricks()    # "Max knows: sit, shake"
dog2.show_tricks()    # "Luna doesn't know any tricks yet."

# Each dog is its OWN object with its OWN data!

# ============================================================
# THE PROJECT: Bank Account Class
# ============================================================

class BankAccount:
    """A bank account with deposit, withdraw, and transfer."""

    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount):
        """Add money to the account."""
        if amount <= 0:
            print("  Deposit amount must be positive!")
            return False

        self.balance += amount
        self._record_transaction("deposit", amount)
        print(f"  Deposited ${amount:,.2f}. New balance: ${self.balance:,.2f}")
        return True

    def withdraw(self, amount):
        """Remove money from the account."""
        if amount <= 0:
            print("  Withdrawal amount must be positive!")
            return False

        if amount > self.balance:
            print(f"  Insufficient funds! Balance: ${self.balance:,.2f}")
            return False

        self.balance -= amount
        self._record_transaction("withdrawal", amount)
        print(f"  Withdrew ${amount:,.2f}. New balance: ${self.balance:,.2f}")
        return True

    def transfer(self, other_account, amount):
        """Transfer money to another account."""
        if self.withdraw(amount):
            other_account.deposit(amount)
            self._record_transaction("transfer out", amount)
            other_account._record_transaction("transfer in", amount)
            print(f"  Transferred ${amount:,.2f} to {other_account.owner}")
            return True
        return False

    def get_history(self):
        """Show transaction history."""
        if not self.transaction_history:
            print("  No transactions yet.")
            return

        print(f"\n  Transaction history for {self.owner}:")
        for t in self.transaction_history:
            print(f"    {t['type']:15s} ${t['amount']:>10,.2f}  (bal: ${t['balance']:>10,.2f})")

    def _record_transaction(self, trans_type, amount):
        """Record a transaction (private method — starts with _)."""
        self.transaction_history.append({
            "type": trans_type,
            "amount": amount,
            "balance": self.balance
        })

    def __str__(self):
        return f"Account({self.owner}, balance=${self.balance:,.2f})"


# --- Main program ---
print("=== BANK ACCOUNT SYSTEM ===\n")

# Create accounts
alice = BankAccount("Alice", 1000)
bob = BankAccount("Bob", 500)

print(alice)  # Account(Alice, balance=$1,000.00)
print(bob)    # Account(Bob, balance=$500.00)

# Interactive menu
accounts = {"alice": alice, "bob": bob}

while True:
    print(f"\n  Accounts: {', '.join(accounts.keys())}")
    print("  1. Deposit")
    print("  2. Withdraw")
    print("  3. Transfer")
    print("  4. Check balance")
    print("  5. Transaction history")
    print("  6. Create new account")
    print("  7. Quit")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        name = input("  Account name: ").lower()
        if name in accounts:
            try:
                amount = float(input("  Amount: $"))
                accounts[name].deposit(amount)
            except ValueError:
                print("  Invalid amount!")
        else:
            print(f"  Account '{name}' not found.")

    elif choice == "2":
        name = input("  Account name: ").lower()
        if name in accounts:
            try:
                amount = float(input("  Amount: $"))
                accounts[name].withdraw(amount)
            except ValueError:
                print("  Invalid amount!")
        else:
            print(f"  Account '{name}' not found.")

    elif choice == "3":
        from_name = input("  From: ").lower()
        to_name = input("  To: ").lower()
        if from_name in accounts and to_name in accounts:
            try:
                amount = float(input("  Amount: $"))
                accounts[from_name].transfer(accounts[to_name], amount)
            except ValueError:
                print("  Invalid amount!")
        else:
            print("  Account not found.")

    elif choice == "4":
        name = input("  Account name: ").lower()
        if name in accounts:
            print(f"\n  {accounts[name]}")
        else:
            print(f"  '{name}' not found.")

    elif choice == "5":
        name = input("  Account name: ").lower()
        if name in accounts:
            accounts[name].get_history()
        else:
            print(f"  '{name}' not found.")

    elif choice == "6":
        name = input("  New account name: ").strip().lower()
        try:
            initial = float(input("  Initial deposit: $") or "0")
        except ValueError:
            initial = 0
        accounts[name] = BankAccount(name.title(), initial)
        print(f"  Created account for {name.title()}!")

    elif choice == "7":
        print("  Goodbye!")
        break

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a SavingsAccount class that earns interest.
# It should have a method apply_interest(rate) that adds interest.

# CHALLENGE 2: Add a minimum balance requirement.
# Don't allow withdrawals that would bring the balance below $50.

# CHALLENGE 3: Add overdraft protection — if a withdrawal exceeds
# the balance, only take what's available and warn the user.

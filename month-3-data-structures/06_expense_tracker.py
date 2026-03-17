"""
PROJECT 06: EXPENSE TRACKER
==============================
Track expenses and save them to a CSV file.

WHAT YOU'LL LEARN:
- Writing to files
- CSV format (Comma-Separated Values)
- JSON format
- Reading data back from files (persistence!)
- The datetime module
"""

import json
from datetime import datetime

# ============================================================
# LESSON: JSON — The universal data format
# ============================================================

# JSON looks almost exactly like Python dictionaries and lists.
# It's used EVERYWHERE — websites, apps, APIs, config files.

data = {
    "name": "Alice",
    "age": 25,
    "hobbies": ["reading", "coding"]
}

# Convert Python dict to JSON string:
json_string = json.dumps(data, indent=2)  # indent=2 makes it pretty
print(json_string)

# Convert JSON string back to Python dict:
parsed = json.loads(json_string)
print(parsed["name"])  # "Alice"

# Save to a JSON file:
with open("example.json", "w") as f:
    json.dump(data, f, indent=2)

# Load from a JSON file:
with open("example.json", "r") as f:
    loaded = json.load(f)
print(loaded)

# ============================================================
# LESSON: The datetime module
# ============================================================

now = datetime.now()
print(now)                              # 2026-03-17 14:30:00.123456
print(now.strftime("%Y-%m-%d"))         # 2026-03-17
print(now.strftime("%B %d, %Y"))        # March 17, 2026
print(now.strftime("%I:%M %p"))         # 02:30 PM

# ============================================================
# THE PROJECT: Expense Tracker
# ============================================================

DATA_FILE = "expenses.json"


def load_expenses():
    """Load expenses from file."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_expenses(expenses):
    """Save expenses to file."""
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses):
    """Add a new expense."""
    try:
        amount = float(input("  Amount: $"))
    except ValueError:
        print("  Invalid amount!")
        return

    category = input("  Category (food/transport/entertainment/bills/other): ").strip().lower()
    description = input("  Description: ").strip()

    expense = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": amount,
        "category": category,
        "description": description
    }

    expenses.append(expense)
    save_expenses(expenses)
    print(f"  Added: ${amount:.2f} for {description}")


def view_expenses(expenses):
    """View all expenses."""
    if not expenses:
        print("  No expenses recorded yet!")
        return

    print(f"\n  === ALL EXPENSES ===\n")
    print(f"  {'Date':<12} {'Category':<15} {'Amount':>8}  {'Description'}")
    print(f"  {'-'*12} {'-'*15} {'-'*8}  {'-'*20}")

    total = 0
    for e in expenses:
        print(f"  {e['date']:<12} {e['category']:<15} ${e['amount']:>7.2f}  {e['description']}")
        total += e["amount"]

    print(f"\n  {'TOTAL:':<28} ${total:>7.2f}")


def summary_by_category(expenses):
    """Show spending breakdown by category."""
    if not expenses:
        print("  No expenses recorded yet!")
        return

    # Sum up each category
    categories = {}
    total = 0
    for e in expenses:
        cat = e["category"]
        if cat in categories:
            categories[cat] += e["amount"]
        else:
            categories[cat] = e["amount"]
        total += e["amount"]

    print(f"\n  === SPENDING BY CATEGORY ===\n")
    for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / total) * 100
        bar = "#" * int(percentage / 2)
        print(f"  {cat:<15} ${amount:>8.2f}  ({percentage:>5.1f}%)  {bar}")

    print(f"\n  {'TOTAL':<15} ${total:>8.2f}")


def monthly_summary(expenses):
    """Show spending per month."""
    if not expenses:
        print("  No expenses yet!")
        return

    months = {}
    for e in expenses:
        month = e["date"][:7]  # "2026-03"
        if month in months:
            months[month] += e["amount"]
        else:
            months[month] = e["amount"]

    print(f"\n  === MONTHLY SPENDING ===\n")
    for month, amount in sorted(months.items()):
        print(f"  {month}: ${amount:.2f}")


# --- Main program ---
print("=== EXPENSE TRACKER ===")
expenses = load_expenses()
print(f"  Loaded {len(expenses)} expenses from file.\n")

while True:
    print("\n  1. Add expense")
    print("  2. View all expenses")
    print("  3. Category summary")
    print("  4. Monthly summary")
    print("  5. Quit")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        add_expense(expenses)
    elif choice == "2":
        view_expenses(expenses)
    elif choice == "3":
        summary_by_category(expenses)
    elif choice == "4":
        monthly_summary(expenses)
    elif choice == "5":
        print(f"  Saved {len(expenses)} expenses. Goodbye!")
        break

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a budget feature. Set monthly budgets per category
# and warn when spending exceeds the budget.

# CHALLENGE 2: Export expenses to a CSV file that can be opened in Excel.
# CSV format: date,amount,category,description

# CHALLENGE 3: Add a "delete expense" feature — show numbered list,
# let user pick one to delete.

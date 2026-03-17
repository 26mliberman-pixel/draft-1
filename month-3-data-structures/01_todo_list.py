"""
PROJECT 01: TO-DO LIST
========================
A fully functional to-do list. Learn LISTS — Python's most useful data structure.

WHAT YOU'LL LEARN:
- Creating lists
- Adding, removing, and accessing items
- Looping through lists
- List methods: append, remove, pop, insert, sort, etc.

LISTS ARE EVERYWHERE IN PROGRAMMING.
A list is an ordered collection of items. It can hold any type of data,
and you can add, remove, or change items at any time.
"""

# ============================================================
# LESSON: Lists basics
# ============================================================

# Creating a list — use square brackets []
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, 3.14, True]  # Can mix types (but usually don't)
empty = []  # An empty list

# Accessing items by INDEX (position) — starts at 0!
print(fruits[0])    # "apple" (first item)
print(fruits[1])    # "banana" (second item)
print(fruits[-1])   # "cherry" (last item)

# How many items? len()
print(len(fruits))  # 3

# ============================================================
# LESSON: Modifying lists
# ============================================================

fruits = ["apple", "banana", "cherry"]

# ADD items:
fruits.append("date")           # Add to the END → ["apple", "banana", "cherry", "date"]
fruits.insert(1, "blueberry")   # Insert at position 1

# REMOVE items:
fruits.remove("banana")  # Remove by VALUE (removes first occurrence)
last = fruits.pop()      # Remove and return the LAST item
first = fruits.pop(0)    # Remove and return item at position 0

# CHANGE an item:
fruits = ["apple", "banana", "cherry"]
fruits[1] = "blackberry"  # Replace "banana" with "blackberry"

# CHECK if something is in the list:
print("apple" in fruits)  # True
print("mango" in fruits)  # False

# SORT:
numbers = [3, 1, 4, 1, 5, 9]
numbers.sort()             # Sorts in place → [1, 1, 3, 4, 5, 9]
numbers.sort(reverse=True) # Descending → [9, 5, 4, 3, 1, 1]

# LOOP through a list:
for fruit in fruits:
    print(f"I like {fruit}")

# Loop with index:
for i, fruit in enumerate(fruits):
    print(f"{i + 1}. {fruit}")

# ============================================================
# THE PROJECT: To-Do List App
# ============================================================

todos = []


def show_todos():
    """Display all to-do items."""
    if not todos:
        print("\n  Your to-do list is empty!")
        return

    print(f"\n  === YOUR TO-DO LIST ({len(todos)} items) ===\n")
    for i, task in enumerate(todos, 1):
        status = "done" if task["done"] else "    "
        print(f"  [{status}] {i}. {task['text']}")
    print()


def add_todo():
    """Add a new to-do item."""
    text = input("  What do you need to do? ").strip()
    if text:
        todos.append({"text": text, "done": False})
        print(f"  Added: '{text}'")
    else:
        print("  Can't add an empty task!")


def complete_todo():
    """Mark a to-do as done."""
    show_todos()
    if not todos:
        return

    try:
        num = int(input("  Which task number is done? "))
        if 1 <= num <= len(todos):
            todos[num - 1]["done"] = True
            print(f"  Completed: '{todos[num - 1]['text']}'")
        else:
            print("  Invalid number!")
    except ValueError:
        print("  Please enter a number!")


def delete_todo():
    """Remove a to-do item."""
    show_todos()
    if not todos:
        return

    try:
        num = int(input("  Which task number to delete? "))
        if 1 <= num <= len(todos):
            removed = todos.pop(num - 1)
            print(f"  Deleted: '{removed['text']}'")
        else:
            print("  Invalid number!")
    except ValueError:
        print("  Please enter a number!")


# --- Main loop ---
print("=== TO-DO LIST APP ===")

while True:
    print("\n  1. View tasks")
    print("  2. Add task")
    print("  3. Complete task")
    print("  4. Delete task")
    print("  5. Quit")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        show_todos()
    elif choice == "2":
        add_todo()
    elif choice == "3":
        complete_todo()
    elif choice == "4":
        delete_todo()
    elif choice == "5":
        print("\n  Goodbye! Don't forget your tasks!")
        break
    else:
        print("  Invalid choice.")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add priorities (high, medium, low) to each task.
# Sort tasks by priority when displaying.

# CHALLENGE 2: Save the to-do list to a file when quitting
# and load it when starting. (You'll learn this in project 06!)

# CHALLENGE 3: Add a "search" feature to find tasks containing a keyword.

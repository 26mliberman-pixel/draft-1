"""
PROJECT 02: CONTACT BOOK
==========================
Store and look up contacts. Learn DICTIONARIES.

WHAT YOU'LL LEARN:
- Dictionaries — the most powerful data structure in Python
- Key-value pairs
- Nested dictionaries
- Dictionary methods

DICTIONARIES are like real dictionaries: you look up a WORD (key)
to find its DEFINITION (value). In Python, the keys and values can
be anything.
"""

# ============================================================
# LESSON: Dictionary basics
# ============================================================

# Creating a dictionary — use curly braces {} with key: value pairs
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}

# Accessing values by key:
print(person["name"])     # "Alice"
print(person["age"])      # 25

# Using .get() — safer (returns None instead of crashing if key doesn't exist)
print(person.get("name"))          # "Alice"
print(person.get("phone"))         # None (no crash!)
print(person.get("phone", "N/A")) # "N/A" (custom default)

# Adding/changing values:
person["email"] = "alice@email.com"  # Add new key
person["age"] = 26                    # Change existing key

# Removing:
del person["city"]                    # Delete a key
removed = person.pop("email")        # Remove and return the value

# Check if key exists:
print("name" in person)  # True
print("phone" in person) # False

# Loop through a dictionary:
person = {"name": "Alice", "age": 25, "city": "NYC"}

for key in person:
    print(f"{key}: {person[key]}")

# Or better:
for key, value in person.items():
    print(f"{key}: {value}")

# Get all keys or all values:
print(list(person.keys()))    # ["name", "age", "city"]
print(list(person.values()))  # ["Alice", 25, "NYC"]

# ============================================================
# THE PROJECT: Contact Book
# ============================================================

contacts = {}


def add_contact():
    """Add a new contact."""
    name = input("  Name: ").strip().title()
    if name in contacts:
        print(f"  '{name}' already exists! Use 'edit' to update.")
        return

    phone = input("  Phone: ").strip()
    email = input("  Email: ").strip()

    contacts[name] = {
        "phone": phone,
        "email": email
    }
    print(f"  Contact '{name}' added!")


def view_contacts():
    """Display all contacts."""
    if not contacts:
        print("\n  No contacts yet!")
        return

    print(f"\n  === CONTACTS ({len(contacts)}) ===\n")
    for name, info in sorted(contacts.items()):
        print(f"  {name}")
        print(f"    Phone: {info['phone']}")
        print(f"    Email: {info['email']}")
        print()


def search_contact():
    """Find a contact by name."""
    query = input("  Search for: ").strip().title()

    found = False
    for name, info in contacts.items():
        if query in name:
            print(f"\n  {name}")
            print(f"    Phone: {info['phone']}")
            print(f"    Email: {info['email']}")
            found = True

    if not found:
        print(f"  No contacts matching '{query}'.")


def delete_contact():
    """Remove a contact."""
    name = input("  Name to delete: ").strip().title()
    if name in contacts:
        del contacts[name]
        print(f"  '{name}' deleted.")
    else:
        print(f"  '{name}' not found.")


def edit_contact():
    """Edit an existing contact."""
    name = input("  Name to edit: ").strip().title()
    if name not in contacts:
        print(f"  '{name}' not found.")
        return

    print(f"  Current phone: {contacts[name]['phone']}")
    new_phone = input("  New phone (Enter to keep): ").strip()
    if new_phone:
        contacts[name]["phone"] = new_phone

    print(f"  Current email: {contacts[name]['email']}")
    new_email = input("  New email (Enter to keep): ").strip()
    if new_email:
        contacts[name]["email"] = new_email

    print(f"  '{name}' updated!")


# --- Main program ---
print("=== CONTACT BOOK ===")

while True:
    print("\n  1. Add contact")
    print("  2. View all contacts")
    print("  3. Search contacts")
    print("  4. Edit contact")
    print("  5. Delete contact")
    print("  6. Quit")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        add_contact()
    elif choice == "2":
        view_contacts()
    elif choice == "3":
        search_contact()
    elif choice == "4":
        edit_contact()
    elif choice == "5":
        delete_contact()
    elif choice == "6":
        print("\n  Goodbye!")
        break

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add more fields — address, birthday, notes.

# CHALLENGE 2: Add an "export" feature that prints all contacts
# in a nicely formatted way (like a printable address book).

# CHALLENGE 3: Save contacts to a JSON file (you'll learn JSON in project 06).

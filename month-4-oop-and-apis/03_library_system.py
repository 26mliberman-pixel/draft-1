"""
PROJECT 03: LIBRARY SYSTEM
==============================
A library with books and members. Learn INHERITANCE.

WHAT YOU'LL LEARN:
- Inheritance — building new classes from existing ones
- super() — calling the parent class
- Overriding methods
- Relationships between classes
"""

# ============================================================
# LESSON: Inheritance
# ============================================================

# Inheritance lets you create a new class based on an existing one.
# The new class INHERITS all the methods and attributes of the parent.

class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        print(f"{self.name} says {self.sound}!")


class Dog(Animal):  # Dog INHERITS from Animal
    def __init__(self, name):
        super().__init__(name, "Woof")  # Call the parent's __init__
        self.tricks = []

    def learn_trick(self, trick):
        self.tricks.append(trick)


class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, "Meow")

    def speak(self):
        # OVERRIDE — replace the parent's method
        print(f"{self.name} says {self.sound}... when it feels like it.")


dog = Dog("Buddy")
cat = Cat("Whiskers")
dog.speak()  # "Buddy says Woof!" (inherited from Animal)
cat.speak()  # "Whiskers says Meow... when it feels like it." (overridden)

# ============================================================
# THE PROJECT: Library System
# ============================================================

from datetime import datetime, timedelta


class LibraryItem:
    """Base class for all library items."""

    def __init__(self, title, item_id):
        self.title = title
        self.item_id = item_id
        self.checked_out = False
        self.due_date = None
        self.checked_out_by = None

    def checkout(self, member_name, days=14):
        if self.checked_out:
            print(f"  '{self.title}' is already checked out!")
            return False
        self.checked_out = True
        self.due_date = datetime.now() + timedelta(days=days)
        self.checked_out_by = member_name
        print(f"  '{self.title}' checked out to {member_name}.")
        print(f"  Due: {self.due_date.strftime('%Y-%m-%d')}")
        return True

    def return_item(self):
        if not self.checked_out:
            print(f"  '{self.title}' is not checked out.")
            return False
        print(f"  '{self.title}' returned by {self.checked_out_by}.")
        self.checked_out = False
        self.due_date = None
        self.checked_out_by = None
        return True

    def __str__(self):
        status = f"OUT (due {self.due_date.strftime('%m/%d')})" if self.checked_out else "Available"
        return f"[{self.item_id}] {self.title} - {status}"


class Book(LibraryItem):
    """A book in the library."""

    def __init__(self, title, author, item_id, pages=0):
        super().__init__(title, item_id)
        self.author = author
        self.pages = pages
        self.item_type = "Book"

    def __str__(self):
        base = super().__str__()
        return f"{base} | by {self.author}"


class DVD(LibraryItem):
    """A DVD in the library."""

    def __init__(self, title, director, item_id, runtime=0):
        super().__init__(title, item_id)
        self.director = director
        self.runtime = runtime
        self.item_type = "DVD"

    def checkout(self, member_name, days=7):  # DVDs have shorter loan period
        return super().checkout(member_name, days)

    def __str__(self):
        base = super().__str__()
        return f"{base} | dir. {self.director} ({self.runtime}min)"


class Member:
    """A library member."""

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.checked_out_items = []

    def __str__(self):
        return f"{self.name} (ID: {self.member_id}) - {len(self.checked_out_items)} items out"


class Library:
    """The library itself — manages items and members."""

    def __init__(self, name):
        self.name = name
        self.items = []
        self.members = []

    def add_item(self, item):
        self.items.append(item)

    def add_member(self, member):
        self.members.append(member)

    def find_item(self, query):
        """Search for items by title (partial match)."""
        results = []
        for item in self.items:
            if query.lower() in item.title.lower():
                results.append(item)
        return results

    def find_member(self, name):
        for m in self.members:
            if m.name.lower() == name.lower():
                return m
        return None

    def checkout_item(self, item_id, member_name):
        member = self.find_member(member_name)
        if not member:
            print(f"  Member '{member_name}' not found.")
            return

        for item in self.items:
            if item.item_id == item_id:
                if item.checkout(member_name):
                    member.checked_out_items.append(item)
                return

        print(f"  Item '{item_id}' not found.")

    def return_item(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                member_name = item.checked_out_by
                if item.return_item():
                    member = self.find_member(member_name)
                    if member and item in member.checked_out_items:
                        member.checked_out_items.remove(item)
                return

        print(f"  Item '{item_id}' not found.")

    def show_catalog(self):
        print(f"\n  === {self.name} Catalog ({len(self.items)} items) ===\n")
        for item in self.items:
            print(f"  {item}")

    def show_members(self):
        print(f"\n  === Members ({len(self.members)}) ===\n")
        for m in self.members:
            print(f"  {m}")


# --- Set up the library ---
lib = Library("Python City Library")

# Add some books and DVDs
lib.add_item(Book("Python Crash Course", "Eric Matthes", "B001", 544))
lib.add_item(Book("Clean Code", "Robert Martin", "B002", 464))
lib.add_item(Book("The Hobbit", "J.R.R. Tolkien", "B003", 310))
lib.add_item(Book("1984", "George Orwell", "B004", 328))
lib.add_item(DVD("The Matrix", "Wachowskis", "D001", 136))
lib.add_item(DVD("Inception", "Christopher Nolan", "D002", 148))

lib.add_member(Member("Alice", "M001"))
lib.add_member(Member("Bob", "M002"))

# --- Main program ---
print(f"=== {lib.name} ===\n")

while True:
    print("\n  1. View catalog")
    print("  2. Search items")
    print("  3. Check out item")
    print("  4. Return item")
    print("  5. View members")
    print("  6. Add member")
    print("  7. Quit")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        lib.show_catalog()
    elif choice == "2":
        query = input("  Search: ")
        results = lib.find_item(query)
        if results:
            for item in results:
                print(f"  {item}")
        else:
            print("  Nothing found.")
    elif choice == "3":
        item_id = input("  Item ID: ").upper()
        member = input("  Member name: ")
        lib.checkout_item(item_id, member)
    elif choice == "4":
        item_id = input("  Item ID: ").upper()
        lib.return_item(item_id)
    elif choice == "5":
        lib.show_members()
    elif choice == "6":
        name = input("  Name: ").strip().title()
        mid = f"M{len(lib.members) + 1:03d}"
        lib.add_member(Member(name, mid))
        print(f"  Added {name} (ID: {mid})")
    elif choice == "7":
        print("  Library closed. Goodbye!")
        break

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a Magazine class that inherits from LibraryItem.
# Magazines can't be checked out — override checkout() to prevent it.

# CHALLENGE 2: Add late fees. If an item is returned after the due date,
# calculate a fee ($0.25/day for books, $1.00/day for DVDs).

# CHALLENGE 3: Save the library state to a JSON file so it persists.

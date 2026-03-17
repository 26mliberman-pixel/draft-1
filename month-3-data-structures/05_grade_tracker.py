"""
PROJECT 05: STUDENT GRADE TRACKER
====================================
Track multiple students and their grades. Learn NESTED data structures.

WHAT YOU'LL LEARN:
- Lists of dictionaries (very common pattern!)
- Nested data structures
- Statistical calculations (average, min, max)
- Sorting complex data
"""

# ============================================================
# LESSON: Nested data structures
# ============================================================

# You can put lists inside dictionaries, dictionaries inside lists, etc.

# List of dictionaries (VERY common in real programming):
students = [
    {"name": "Alice", "grades": [90, 85, 92, 88]},
    {"name": "Bob", "grades": [78, 82, 75, 80]},
    {"name": "Charlie", "grades": [95, 98, 92, 97]},
]

# Accessing nested data:
print(students[0]["name"])       # "Alice"
print(students[0]["grades"][2])  # 92 (Alice's 3rd grade)

# ============================================================
# LESSON: Useful built-in functions for numbers
# ============================================================

numbers = [90, 85, 92, 88]
print(sum(numbers))    # 355 (total)
print(min(numbers))    # 85 (smallest)
print(max(numbers))    # 92 (largest)
print(len(numbers))    # 4 (count)
print(sum(numbers) / len(numbers))  # 88.75 (average)

# ============================================================
# THE PROJECT: Grade Tracker
# ============================================================

students = []


def add_student():
    """Add a new student."""
    name = input("  Student name: ").strip().title()

    for s in students:
        if s["name"] == name:
            print(f"  '{name}' already exists!")
            return

    students.append({"name": name, "grades": []})
    print(f"  Added '{name}'!")


def add_grade():
    """Add a grade for a student."""
    if not students:
        print("  No students yet!")
        return

    name = input("  Student name: ").strip().title()

    for s in students:
        if s["name"] == name:
            try:
                grade = float(input(f"  Grade for {name} (0-100): "))
                if 0 <= grade <= 100:
                    s["grades"].append(grade)
                    print(f"  Added grade {grade} for {name}.")
                else:
                    print("  Grade must be between 0 and 100!")
            except ValueError:
                print("  Invalid grade!")
            return

    print(f"  Student '{name}' not found.")


def get_letter_grade(average):
    """Convert a numeric average to a letter grade."""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def view_student():
    """View detailed info for one student."""
    name = input("  Student name: ").strip().title()

    for s in students:
        if s["name"] == name:
            print(f"\n  === {name} ===")
            if not s["grades"]:
                print("  No grades yet.")
                return

            print(f"  Grades: {s['grades']}")
            avg = sum(s["grades"]) / len(s["grades"])
            print(f"  Average: {avg:.1f}")
            print(f"  Letter:  {get_letter_grade(avg)}")
            print(f"  Highest: {max(s['grades'])}")
            print(f"  Lowest:  {min(s['grades'])}")
            print(f"  # of grades: {len(s['grades'])}")
            return

    print(f"  '{name}' not found.")


def class_report():
    """Show a report for all students."""
    if not students:
        print("  No students yet!")
        return

    print(f"\n  === CLASS REPORT ({len(students)} students) ===\n")
    print(f"  {'Name':<15} {'Avg':>6} {'Grade':>6} {'# Tests':>8}")
    print(f"  {'-'*15} {'-'*6} {'-'*6} {'-'*8}")

    all_averages = []

    for s in sorted(students, key=lambda x: x["name"]):
        name = s["name"]
        if s["grades"]:
            avg = sum(s["grades"]) / len(s["grades"])
            letter = get_letter_grade(avg)
            num = len(s["grades"])
            all_averages.append(avg)
            print(f"  {name:<15} {avg:>6.1f} {letter:>6} {num:>8}")
        else:
            print(f"  {name:<15} {'N/A':>6} {'N/A':>6} {'0':>8}")

    if all_averages:
        print(f"\n  Class average: {sum(all_averages)/len(all_averages):.1f}")
        print(f"  Highest avg:   {max(all_averages):.1f}")
        print(f"  Lowest avg:    {min(all_averages):.1f}")


# --- Main program ---
print("=== STUDENT GRADE TRACKER ===")

while True:
    print("\n  1. Add student")
    print("  2. Add grade")
    print("  3. View student details")
    print("  4. Class report")
    print("  5. Quit")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        add_student()
    elif choice == "2":
        add_grade()
    elif choice == "3":
        view_student()
    elif choice == "4":
        class_report()
    elif choice == "5":
        print("  Goodbye!")
        break

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a "curve" feature — add X points to everyone's
# lowest grade, where X is how far the class average is from 80.

# CHALLENGE 2: Show a histogram of grade distribution:
# A: ####  (4 students)
# B: ######  (6 students)
# etc.

# CHALLENGE 3: Add assignment names. Instead of just numbers,
# each grade has a name like "Midterm", "Quiz 1", etc.

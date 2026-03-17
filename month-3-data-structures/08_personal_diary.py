"""
PROJECT 08: PERSONAL DIARY
==============================
A diary app with full CRUD. Your Month 3 capstone!

WHAT YOU'LL LEARN:
- CRUD operations (Create, Read, Update, Delete)
- Persistent data storage with JSON
- Searching and filtering data
- Combining everything from Month 3

CRUD is the foundation of almost every app:
- Create: Add new data
- Read: View existing data
- Update: Change existing data
- Delete: Remove data
"""

import json
from datetime import datetime

DATA_FILE = "diary.json"


def load_diary():
    """Load diary entries from file."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_diary(entries):
    """Save diary entries to file."""
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def create_entry(entries):
    """CREATE — Write a new diary entry."""
    print("\n  === NEW ENTRY ===")
    print("  Write your entry. Type 'DONE' on a new line when finished.\n")

    lines = []
    while True:
        line = input("  ")
        if line.strip().upper() == "DONE":
            break
        lines.append(line)

    if not lines:
        print("  Empty entry. Nothing saved.")
        return

    mood = input("\n  How are you feeling? (happy/sad/neutral/excited/tired): ").strip().lower()
    tags = input("  Tags (comma-separated, e.g., work,personal): ").strip().split(",")
    tags = [t.strip() for t in tags if t.strip()]

    entry = {
        "id": len(entries) + 1,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "content": "\n".join(lines),
        "mood": mood,
        "tags": tags
    }

    entries.append(entry)
    save_diary(entries)
    print(f"\n  Entry saved! (Entry #{entry['id']})")


def read_entries(entries):
    """READ — View diary entries."""
    if not entries:
        print("  No entries yet. Start writing!")
        return

    print(f"\n  === DIARY ({len(entries)} entries) ===\n")
    for e in entries:
        print(f"  --- Entry #{e['id']} | {e['date']} | Mood: {e['mood']} ---")
        # Show first 80 chars as preview
        preview = e["content"][:80]
        if len(e["content"]) > 80:
            preview += "..."
        print(f"  {preview}")
        if e["tags"]:
            print(f"  Tags: {', '.join(e['tags'])}")
        print()


def read_full_entry(entries):
    """Read a single entry in full."""
    if not entries:
        print("  No entries yet!")
        return

    try:
        entry_id = int(input("  Entry number to read: "))
    except ValueError:
        print("  Invalid number!")
        return

    for e in entries:
        if e["id"] == entry_id:
            print(f"\n  === Entry #{e['id']} ===")
            print(f"  Date: {e['date']}")
            print(f"  Mood: {e['mood']}")
            print(f"  Tags: {', '.join(e['tags']) if e['tags'] else 'none'}")
            print(f"\n{e['content']}\n")
            return

    print(f"  Entry #{entry_id} not found.")


def update_entry(entries):
    """UPDATE — Edit an existing entry."""
    if not entries:
        print("  No entries to edit!")
        return

    read_entries(entries)
    try:
        entry_id = int(input("  Which entry to edit? "))
    except ValueError:
        print("  Invalid number!")
        return

    for e in entries:
        if e["id"] == entry_id:
            print(f"\n  Current content:\n{e['content']}\n")
            print("  Type new content (or 'KEEP' to keep current):")

            lines = []
            while True:
                line = input("  ")
                if line.strip().upper() == "DONE":
                    break
                if line.strip().upper() == "KEEP":
                    print("  Content kept as is.")
                    return
                lines.append(line)

            if lines:
                e["content"] = "\n".join(lines)
                e["date"] = datetime.now().strftime("%Y-%m-%d %H:%M") + " (edited)"
                save_diary(entries)
                print("  Entry updated!")
            return

    print(f"  Entry #{entry_id} not found.")


def delete_entry(entries):
    """DELETE — Remove a diary entry."""
    if not entries:
        print("  No entries to delete!")
        return

    read_entries(entries)
    try:
        entry_id = int(input("  Which entry to delete? "))
    except ValueError:
        print("  Invalid number!")
        return

    for i, e in enumerate(entries):
        if e["id"] == entry_id:
            confirm = input(f"  Delete entry #{entry_id}? (yes/no): ").lower()
            if confirm == "yes":
                entries.pop(i)
                save_diary(entries)
                print("  Entry deleted.")
            else:
                print("  Cancelled.")
            return

    print(f"  Entry #{entry_id} not found.")


def search_entries(entries):
    """Search entries by keyword or tag."""
    if not entries:
        print("  No entries to search!")
        return

    query = input("  Search for: ").strip().lower()
    results = []

    for e in entries:
        if (query in e["content"].lower() or
            query in e["mood"].lower() or
            query in " ".join(e["tags"]).lower()):
            results.append(e)

    if results:
        print(f"\n  Found {len(results)} matching entries:\n")
        for e in results:
            print(f"  #{e['id']} | {e['date']} | {e['content'][:60]}...")
    else:
        print(f"  No entries matching '{query}'.")


def mood_summary(entries):
    """Show mood statistics."""
    if not entries:
        print("  No entries yet!")
        return

    moods = {}
    for e in entries:
        mood = e["mood"]
        moods[mood] = moods.get(mood, 0) + 1

    print(f"\n  === MOOD SUMMARY ===\n")
    for mood, count in sorted(moods.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * count
        print(f"  {mood:<12} {bar} ({count})")


# --- Main program ---
print("=" * 40)
print("  MY PERSONAL DIARY")
print("=" * 40)

entries = load_diary()
print(f"  Loaded {len(entries)} entries.\n")

while True:
    print("  1. Write new entry")
    print("  2. View all entries")
    print("  3. Read full entry")
    print("  4. Edit entry")
    print("  5. Delete entry")
    print("  6. Search")
    print("  7. Mood summary")
    print("  8. Quit")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        create_entry(entries)
    elif choice == "2":
        read_entries(entries)
    elif choice == "3":
        read_full_entry(entries)
    elif choice == "4":
        update_entry(entries)
    elif choice == "5":
        delete_entry(entries)
    elif choice == "6":
        search_entries(entries)
    elif choice == "7":
        mood_summary(entries)
    elif choice == "8":
        print("\n  Your secrets are safe with me. Goodbye!\n")
        break

print("""
  ============================================
  CONGRATULATIONS! You've completed Month 3!

  You now know:
  - Lists, dictionaries, tuples, and sets
  - Reading and writing files
  - JSON data format
  - Processing and analyzing data
  - Building CRUD applications
  - Persistent data storage

  Next up: month-4-oop-and-apis/
  You'll learn about classes, objects, and
  how to talk to the internet!
  ============================================
""")

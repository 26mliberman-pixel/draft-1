"""
PROJECT 07: AUTOMATED FILE ORGANIZER
=======================================
Organize messy folders automatically! Your Month 4 capstone.

WHAT YOU'LL LEARN:
- The os module — interacting with the file system
- os.path — working with file paths
- shutil — moving and copying files
- Real-world automation!

THIS IS A REAL TOOL YOU'LL ACTUALLY USE.
Point it at your Downloads folder and watch it clean up.
"""

import os
import shutil
from datetime import datetime

# ============================================================
# LESSON: The os module
# ============================================================

# os.listdir(path)         — list files in a directory
# os.path.exists(path)     — check if a file/folder exists
# os.path.isfile(path)     — is it a file?
# os.path.isdir(path)      — is it a directory?
# os.path.join(a, b)       — join path parts: "folder" + "file.txt" → "folder/file.txt"
# os.path.splitext(name)   — split extension: "photo.jpg" → ("photo", ".jpg")
# os.path.getsize(path)    — file size in bytes
# os.makedirs(path, exist_ok=True) — create directories (and parents)
# shutil.move(src, dst)    — move a file
# shutil.copy2(src, dst)   — copy a file (preserving metadata)

# ============================================================
# THE PROJECT: File Organizer
# ============================================================

# Map file extensions to folder names
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xlsx", ".xls", ".csv", ".pptx"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs"],
    "Executables": [".exe", ".msi", ".dmg", ".app", ".deb", ".rpm"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "Data": [".json", ".xml", ".yaml", ".yml", ".sql", ".db"],
}


def get_category(filename):
    """Determine which category a file belongs to."""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category

    return "Other"


def format_size(bytes_size):
    """Convert bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"


def scan_directory(path):
    """Scan a directory and show what would be organized."""
    if not os.path.isdir(path):
        print(f"  '{path}' is not a valid directory!")
        return {}

    plan = {}  # category → list of files

    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)

        # Skip directories, hidden files, and this script
        if os.path.isdir(filepath) or filename.startswith("."):
            continue

        category = get_category(filename)
        if category not in plan:
            plan[category] = []

        size = os.path.getsize(filepath)
        plan[category].append({
            "name": filename,
            "path": filepath,
            "size": size
        })

    return plan


def show_plan(plan):
    """Display the organization plan."""
    if not plan:
        print("  No files to organize!")
        return

    total_files = 0
    print(f"\n  === ORGANIZATION PLAN ===\n")

    for category, files in sorted(plan.items()):
        total_size = sum(f["size"] for f in files)
        print(f"  📁 {category}/ ({len(files)} files, {format_size(total_size)})")
        for f in files[:5]:  # Show first 5 files
            print(f"      {f['name']} ({format_size(f['size'])})")
        if len(files) > 5:
            print(f"      ... and {len(files) - 5} more")
        print()
        total_files += len(files)

    print(f"  Total: {total_files} files into {len(plan)} folders")


def organize_files(source_path, plan):
    """Actually move the files into organized folders."""
    moved = 0
    errors = 0

    for category, files in plan.items():
        # Create the category folder
        dest_folder = os.path.join(source_path, category)
        os.makedirs(dest_folder, exist_ok=True)

        for f in files:
            try:
                dest_path = os.path.join(dest_folder, f["name"])

                # Handle duplicate filenames
                if os.path.exists(dest_path):
                    name, ext = os.path.splitext(f["name"])
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    dest_path = os.path.join(dest_folder, f"{name}_{timestamp}{ext}")

                shutil.move(f["path"], dest_path)
                moved += 1
            except Exception as e:
                print(f"  Error moving {f['name']}: {e}")
                errors += 1

    print(f"\n  Done! Moved {moved} files. Errors: {errors}")


def undo_organize(path):
    """Move all files back to the parent directory."""
    moved = 0

    for category in FILE_CATEGORIES.keys():
        folder = os.path.join(path, category)
        if not os.path.isdir(folder):
            continue

        for filename in os.listdir(folder):
            src = os.path.join(folder, filename)
            dst = os.path.join(path, filename)
            if os.path.isfile(src):
                shutil.move(src, dst)
                moved += 1

        # Remove empty folder
        if not os.listdir(folder):
            os.rmdir(folder)

    # Check "Other" folder too
    other_folder = os.path.join(path, "Other")
    if os.path.isdir(other_folder):
        for filename in os.listdir(other_folder):
            src = os.path.join(other_folder, filename)
            dst = os.path.join(path, filename)
            if os.path.isfile(src):
                shutil.move(src, dst)
                moved += 1
        if not os.listdir(other_folder):
            os.rmdir(other_folder)

    print(f"  Undone! Moved {moved} files back.")


# --- Main program ---
print("=== FILE ORGANIZER ===")
print("  Automatically organize files into folders by type.\n")

while True:
    print("  1. Scan a directory (preview)")
    print("  2. Organize files")
    print("  3. Undo organization")
    print("  4. Quit")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        path = input("  Directory path (or '.' for current): ").strip() or "."
        plan = scan_directory(path)
        show_plan(plan)

    elif choice == "2":
        path = input("  Directory to organize: ").strip() or "."
        plan = scan_directory(path)
        show_plan(plan)

        if plan:
            confirm = input("\n  Proceed? (yes/no): ").lower()
            if confirm == "yes":
                organize_files(path, plan)
            else:
                print("  Cancelled.")

    elif choice == "3":
        path = input("  Directory to un-organize: ").strip() or "."
        confirm = input("  Move all files back to parent? (yes/no): ").lower()
        if confirm == "yes":
            undo_organize(path)

    elif choice == "4":
        print("  Keep it tidy! Goodbye!")
        break

print("""
  ============================================
  CONGRATULATIONS! You've completed Month 4!

  You now know:
  - Classes and objects (OOP)
  - Inheritance and polymorphism
  - APIs and HTTP requests
  - JSON data from the web
  - Command-line tools with argparse
  - File system operations with os
  - Real-world automation!

  Next up: month-5-web-and-databases/
  You'll build web applications!
  ============================================
""")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a "sort by date" option — organize files into
# YYYY/MM/ folders based on when they were created.

# CHALLENGE 2: Add a "find duplicates" feature — find files with
# the same name or same size.

# CHALLENGE 3: Add a "dry run" mode that shows what WOULD happen
# without actually moving anything (we partially did this already).

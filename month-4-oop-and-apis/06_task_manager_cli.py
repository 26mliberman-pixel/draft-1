"""
PROJECT 06: CLI TASK MANAGER
================================
A command-line task manager. Learn MODULES and ARGPARSE.

WHAT YOU'LL LEARN:
- Creating your own modules (splitting code into files)
- argparse — building proper command-line tools
- pip — installing third-party packages
- The sys module

WHAT IS A MODULE?
A module is just a .py file that contains code you can import.
When you did "import random", you were importing the random MODULE.
You can make your own!

WHAT IS ARGPARSE?
argparse lets you create command-line tools that take arguments.
Like: python task_manager.py add "Buy groceries" --priority high
"""

import argparse
import json
from datetime import datetime

# ============================================================
# LESSON: argparse — Command-line arguments
# ============================================================

# Instead of a menu-based app, this uses command-line arguments:
# python 06_task_manager_cli.py add "Buy milk"
# python 06_task_manager_cli.py list
# python 06_task_manager_cli.py done 1

DATA_FILE = "tasks.json"


def load_tasks():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(args):
    """Add a new task."""
    tasks = load_tasks()

    task = {
        "id": len(tasks) + 1,
        "text": args.text,
        "priority": args.priority,
        "done": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"  Added task #{task['id']}: {task['text']} [{task['priority']}]")


def list_tasks(args):
    """List all tasks."""
    tasks = load_tasks()

    if not tasks:
        print("  No tasks! Use 'add' to create one.")
        return

    # Filter by status
    if hasattr(args, "show") and args.show == "done":
        tasks = [t for t in tasks if t["done"]]
    elif hasattr(args, "show") and args.show == "pending":
        tasks = [t for t in tasks if not t["done"]]

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda t: priority_order.get(t["priority"], 1))

    print(f"\n  {'ID':<4} {'Status':<8} {'Priority':<10} {'Task'}")
    print(f"  {'-'*4} {'-'*8} {'-'*10} {'-'*30}")

    for t in tasks:
        status = "[done]" if t["done"] else "[    ]"
        print(f"  {t['id']:<4} {status:<8} {t['priority']:<10} {t['text']}")


def done_task(args):
    """Mark a task as done."""
    tasks = load_tasks()

    for t in tasks:
        if t["id"] == args.id:
            t["done"] = True
            save_tasks(tasks)
            print(f"  Completed: {t['text']}")
            return

    print(f"  Task #{args.id} not found.")


def delete_task(args):
    """Delete a task."""
    tasks = load_tasks()
    original_len = len(tasks)
    tasks = [t for t in tasks if t["id"] != args.id]

    if len(tasks) < original_len:
        save_tasks(tasks)
        print(f"  Deleted task #{args.id}")
    else:
        print(f"  Task #{args.id} not found.")


# ============================================================
# Set up the argument parser
# ============================================================

parser = argparse.ArgumentParser(
    description="CLI Task Manager — manage your tasks from the terminal!"
)
subparsers = parser.add_subparsers(dest="command", help="Available commands")

# "add" command
add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("text", help="The task description")
add_parser.add_argument(
    "--priority", "-p",
    choices=["high", "medium", "low"],
    default="medium",
    help="Task priority (default: medium)"
)

# "list" command
list_parser = subparsers.add_parser("list", help="List all tasks")
list_parser.add_argument(
    "--show", "-s",
    choices=["all", "done", "pending"],
    default="all",
    help="Filter tasks by status"
)

# "done" command
done_parser = subparsers.add_parser("done", help="Mark a task as done")
done_parser.add_argument("id", type=int, help="Task ID to mark as done")

# "delete" command
del_parser = subparsers.add_parser("delete", help="Delete a task")
del_parser.add_argument("id", type=int, help="Task ID to delete")

# Parse and execute
args = parser.parse_args()

if args.command == "add":
    add_task(args)
elif args.command == "list":
    list_tasks(args)
elif args.command == "done":
    done_task(args)
elif args.command == "delete":
    delete_task(args)
else:
    parser.print_help()
    print("\nExamples:")
    print('  python 06_task_manager_cli.py add "Buy groceries" -p high')
    print("  python 06_task_manager_cli.py list")
    print("  python 06_task_manager_cli.py list --show pending")
    print("  python 06_task_manager_cli.py done 1")
    print("  python 06_task_manager_cli.py delete 1")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a "search" command to find tasks by keyword.

# CHALLENGE 2: Add due dates. "add 'Finish report' --due 2026-03-20"
# Show overdue tasks in the list.

# CHALLENGE 3: Add tags/categories. "add 'Call mom' --tag personal"
# Filter by tag: "list --tag work"

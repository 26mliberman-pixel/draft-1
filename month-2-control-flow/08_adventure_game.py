"""
PROJECT 08: MINI TEXT ADVENTURE GAME
=======================================
A choose-your-own-adventure game. Your Month 2 capstone!

WHAT YOU'LL LEARN:
- Functions calling other functions
- Complex decision trees
- Game design thinking
- Organizing a bigger program

THIS IS YOUR BIGGEST PROJECT YET. Take your time. Have fun with it.
"""

import time
import random


def slow_print(text, delay=0.03):
    """Print text one character at a time for dramatic effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # New line at the end


def get_choice(options):
    """Display options and get a valid choice from the player."""
    print()
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    print()

    while True:
        choice = input("  Your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        print(f"  Please enter a number between 1 and {len(options)}.")


def intro():
    """The opening scene."""
    print("\n" + "=" * 50)
    print("  THE DUNGEON OF DECISIONS")
    print("=" * 50)

    slow_print("\nYou wake up in a dark, cold room.")
    slow_print("The last thing you remember is walking home from work.")
    slow_print("Now you're lying on a stone floor.")
    slow_print("As your eyes adjust, you see two doors ahead of you.")
    slow_print("A faint glow comes from under the LEFT door.")
    slow_print("Strange sounds come from behind the RIGHT door.")

    choice = get_choice([
        "Go through the LEFT door (glowing light)",
        "Go through the RIGHT door (strange sounds)",
        "Stay put and yell for help"
    ])

    if choice == 1:
        left_door()
    elif choice == 2:
        right_door()
    else:
        stay_put()


def left_door():
    """The left door path — a library."""
    slow_print("\nYou push open the left door...")
    slow_print("It's a massive underground library!")
    slow_print("Bookshelves reach from floor to ceiling.")
    slow_print("In the center, an old wizard sits reading a book.")
    slow_print('He looks up and says: "Ah, a visitor! I can help you escape."')
    slow_print('"But first, you must answer my riddle."')

    print('\nThe wizard asks: "I have cities, but no houses.')
    print('I have mountains, but no trees.')
    print('I have water, but no fish. What am I?"')

    choice = get_choice([
        "A map",
        "A painting",
        "A dream",
        "A globe"
    ])

    if choice == 1 or choice == 4:  # Map or globe — both acceptable
        wizard_happy()
    else:
        wizard_disappointed()


def right_door():
    """The right door path — a creature."""
    slow_print("\nYou push open the right door...")
    slow_print("You enter a large cave with a underground river.")
    slow_print("Sitting by the river is a friendly-looking dragon.")
    slow_print('The dragon says: "Hey! I\'m Doug. I\'m stuck down here too."')
    slow_print('"I could fly us out, but I need something to eat first."')
    slow_print('"I see some mushrooms by the river and a chest in the corner."')

    choice = get_choice([
        "Offer the mushrooms to Doug",
        "Open the chest",
        "Try to ride Doug without feeding him"
    ])

    if choice == 1:
        feed_dragon()
    elif choice == 2:
        open_chest()
    else:
        angry_dragon()


def stay_put():
    """Staying in the starting room."""
    slow_print("\nYou yell 'HELLO? ANYONE THERE?'")
    slow_print("...")
    slow_print("Echo answers back... then silence.")
    slow_print("After a while, you notice something on the wall.")
    slow_print("It's a message scratched into the stone:")
    slow_print('"THE ONLY WAY OUT IS FORWARD."')
    slow_print("\nYou realize you need to pick a door.")

    choice = get_choice([
        "Go through the LEFT door",
        "Go through the RIGHT door"
    ])

    if choice == 1:
        left_door()
    else:
        right_door()


def wizard_happy():
    """The wizard is pleased with your answer."""
    slow_print('\nThe wizard smiles. "Correct! You are clever."')
    slow_print('He waves his staff and a portal appears.')
    slow_print('"This will take you home. But take this first."')
    slow_print("He hands you a small glowing stone.")
    slow_print('"It will light your way whenever you feel lost."')
    slow_print("\nYou step through the portal...")
    ending_good()


def wizard_disappointed():
    """Wrong answer for the wizard."""
    slow_print('\nThe wizard frowns. "Incorrect, I\'m afraid."')
    slow_print('"But I am not cruel. Here\'s another chance."')
    slow_print('"Behind me are two passages. One leads out."')
    slow_print('"The other leads... deeper."')

    choice = get_choice([
        "Take the passage on the left",
        "Take the passage on the right"
    ])

    if random.choice([True, False]):  # 50/50 chance
        slow_print("\nThe passage leads to a ladder going UP!")
        slow_print("You climb and climb until you reach fresh air!")
        ending_good()
    else:
        slow_print("\nThe passage twists and turns...")
        slow_print("You end up right back where you started!")
        slow_print("But wait — the other door is still there.\n")
        right_door()


def feed_dragon():
    """Feed the dragon mushrooms."""
    slow_print('\nYou gather the mushrooms and offer them to Doug.')
    slow_print('"Oh, these are my favorite! Thanks, friend!"')
    slow_print("Doug munches happily, then stretches his wings.")
    slow_print('"Hop on! Let\'s get out of here!"')
    slow_print("\nYou climb onto Doug's back.")
    slow_print("He launches into the air, flying through a hole in the cave ceiling.")
    slow_print("The wind rushes past as you soar above the mountains.")
    ending_good()


def open_chest():
    """Open the mysterious chest."""
    slow_print("\nYou walk to the chest and open it slowly...")
    slow_print("Inside you find: a sandwich and a key!")
    slow_print('"Hey, is that a sandwich?" Doug asks, drooling.')

    choice = get_choice([
        "Give Doug the sandwich and keep the key",
        "Keep everything for yourself"
    ])

    if choice == 1:
        slow_print("\nDoug eats the sandwich in one bite.")
        slow_print('"You\'re alright, human! Hop on!"')
        slow_print("You also notice the key fits a small door in the cave wall...")
        slow_print("But Doug is ready to fly! You hop on and soar to freedom!")
        ending_good()
    else:
        slow_print("\nDoug looks sad. You eat the sandwich.")
        slow_print("It's pretty good actually.")
        slow_print("You try the key on every surface in the cave...")
        slow_print("It fits a small hidden door!")
        slow_print("Behind it: a long stairway leading up to daylight!")
        ending_good()


def angry_dragon():
    """Try to ride the hungry dragon."""
    slow_print("\nYou try to jump on Doug's back.")
    slow_print('"HEY! Rude! I said I need to eat first!"')
    slow_print("Doug shakes you off gently but firmly.")
    slow_print('"Tell you what — bring me food and we\'ll try again."')

    choice = get_choice([
        "Gather mushrooms for Doug",
        "Check the chest for food"
    ])

    if choice == 1:
        feed_dragon()
    else:
        open_chest()


def ending_good():
    """The good ending."""
    print("\n" + "=" * 50)
    slow_print("  You made it out! Sunshine hits your face.")
    slow_print("  You take a deep breath of fresh air.")
    slow_print("  You're free!")
    print("=" * 50)
    print("\n  *** THE END ***")
    print("\n  Thanks for playing The Dungeon of Decisions!")


# ============================================================
# START THE GAME
# ============================================================

name = input("\nWhat is your name, adventurer? ")
slow_print(f"\nWelcome, {name}. Your adventure begins now...")

intro()

print("\n" + "=" * 50)
print("  CONGRATULATIONS!")
print("  You've completed Month 2!")
print("=" * 50)
print("""
  You now know:
  - if/elif/else (making decisions)
  - while and for loops (repeating things)
  - functions (reusable code blocks)
  - try/except (handling errors)
  - random module (randomness)
  - time module (pausing, measuring time)
  - Building real programs from scratch!

  Next up: month-3-data-structures/
  You'll learn lists, dictionaries, and file I/O!
""")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add MORE rooms and paths to make the game longer.
# Add at least 3 more decision points.

# CHALLENGE 2: Add an inventory system — pick up items and use them later.
# (Hint: use a list to store inventory items)

# CHALLENGE 3: Add a health system. Some choices reduce health.
# If health reaches 0, game over!

# CHALLENGE 4 (BIG): Create your OWN adventure game with a completely
# different theme (space, underwater, haunted house, zombie apocalypse, etc.)

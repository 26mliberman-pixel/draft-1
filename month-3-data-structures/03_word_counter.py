"""
PROJECT 03: WORD COUNTER
==========================
Count words, letters, and sentences in text. Learn FILE READING.

WHAT YOU'LL LEARN:
- Opening and reading files
- The "with" statement
- String splitting and processing
- Counting with dictionaries
"""

# ============================================================
# LESSON: Reading files
# ============================================================

# First, let's CREATE a sample file to work with.
# (In real life, you'd read existing files.)

sample_text = """Python is a programming language that lets you work quickly
and integrate systems more effectively. Python is powerful and fast,
plays well with others, runs everywhere, is friendly and easy to learn,
and is open source. Python can be used for web development,
data analysis, artificial intelligence, scientific computing,
and automation. Many beginners choose Python as their first
programming language because of its simple syntax."""

# Writing a file:
with open("sample.txt", "w") as f:
    f.write(sample_text)
print("Created sample.txt!")

# Reading a file:
with open("sample.txt", "r") as f:
    content = f.read()   # Reads the ENTIRE file as one big string
print(content)

# Reading line by line:
with open("sample.txt", "r") as f:
    for line in f:
        print(line.strip())  # .strip() removes the newline at the end

# ============================================================
# LESSON: The "with" statement
# ============================================================

# "with open(...) as f:" automatically CLOSES the file when you're done.
# This is important! If you don't close files, bad things can happen.
#
# The old (worse) way:
#   f = open("file.txt", "r")
#   content = f.read()
#   f.close()   ← Easy to forget this!
#
# The "with" way automatically closes it. Always use "with".

# ============================================================
# LESSON: File modes
# ============================================================

# "r"  — Read (default). File must exist.
# "w"  — Write. Creates file if it doesn't exist. OVERWRITES if it does!
# "a"  — Append. Adds to the end of the file.
# "r+" — Read and write.

# ============================================================
# THE PROJECT: Word Counter
# ============================================================

def count_words(text):
    """Count the number of words in text."""
    words = text.split()  # Split on whitespace
    return len(words)


def count_characters(text):
    """Count characters (with and without spaces)."""
    with_spaces = len(text)
    without_spaces = len(text.replace(" ", "").replace("\n", ""))
    return with_spaces, without_spaces


def count_sentences(text):
    """Count sentences (roughly — by counting periods, !, and ?)."""
    count = 0
    for char in text:
        if char in ".!?":
            count += 1
    return count


def word_frequency(text):
    """Count how many times each word appears."""
    words = text.lower().split()
    # Clean up punctuation from words
    cleaned_words = []
    for word in words:
        clean = word.strip(".,!?;:'\"()-")
        if clean:
            cleaned_words.append(clean)

    # Count each word using a dictionary
    freq = {}
    for word in cleaned_words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1

    return freq


def analyze_text(text):
    """Run all analyses on the text."""
    print("\n=== TEXT ANALYSIS ===\n")

    # Basic counts
    words = count_words(text)
    chars_with, chars_without = count_characters(text)
    sentences = count_sentences(text)

    print(f"  Words:                {words}")
    print(f"  Characters (spaces):  {chars_with}")
    print(f"  Characters (no space):{chars_without}")
    print(f"  Sentences:            {sentences}")
    if sentences > 0:
        print(f"  Avg words/sentence:   {round(words / sentences, 1)}")

    # Word frequency
    freq = word_frequency(text)

    # Sort by frequency (most common first)
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    print(f"\n  Top 10 most common words:")
    for word, count in sorted_words[:10]:
        bar = "#" * count
        print(f"    {word:15s} {count:3d} {bar}")


# --- Main program ---
print("=== WORD COUNTER ===\n")
print("  1. Analyze sample.txt")
print("  2. Type your own text")
print("  3. Analyze a file (enter filename)")

choice = input("\n  Choice: ").strip()

if choice == "1":
    with open("sample.txt", "r") as f:
        text = f.read()
    analyze_text(text)
elif choice == "2":
    print("  Type your text (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    text = "\n".join(lines)
    analyze_text(text)
elif choice == "3":
    filename = input("  Filename: ").strip()
    try:
        with open(filename, "r") as f:
            text = f.read()
        analyze_text(text)
    except FileNotFoundError:
        print(f"  File '{filename}' not found!")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a "unique words" count (how many different words).
# Hint: use a set() — it only stores unique items.

# CHALLENGE 2: Find the longest and shortest words in the text.

# CHALLENGE 3: Add a readability score. Simple version:
# If avg words per sentence > 20, it's "hard to read".
# If avg word length > 6 characters, it's "complex vocabulary".

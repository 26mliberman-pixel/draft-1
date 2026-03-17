"""
PROJECT 05: RECIPE FINDER
============================
Search for recipes using a free API.

WHAT YOU'LL LEARN:
- Working with a more complex API
- Processing API response data
- Building a useful real-world tool

SETUP: pip install requests

This uses TheMealDB — a free API with no key required.
"""

import requests

BASE_URL = "https://www.themealdb.com/api/json/v1/1"


def search_by_name(name):
    """Search for recipes by name."""
    try:
        response = requests.get(f"{BASE_URL}/search.php?s={name}", timeout=10)
        data = response.json()
        return data.get("meals") or []
    except requests.exceptions.RequestException as e:
        print(f"  Error: {e}")
        return []


def get_random_recipe():
    """Get a random recipe."""
    try:
        response = requests.get(f"{BASE_URL}/random.php", timeout=10)
        data = response.json()
        meals = data.get("meals")
        return meals[0] if meals else None
    except requests.exceptions.RequestException:
        return None


def search_by_category(category):
    """List meals in a category."""
    try:
        response = requests.get(f"{BASE_URL}/filter.php?c={category}", timeout=10)
        data = response.json()
        return data.get("meals") or []
    except requests.exceptions.RequestException:
        return []


def get_categories():
    """Get list of all categories."""
    try:
        response = requests.get(f"{BASE_URL}/categories.php", timeout=10)
        data = response.json()
        return data.get("categories") or []
    except requests.exceptions.RequestException:
        return []


def display_recipe(meal):
    """Display a recipe in a nice format."""
    if not meal:
        print("  No recipe found.")
        return

    print(f"\n  ╔{'═' * 48}╗")
    print(f"  ║ {meal['strMeal'][:46]:^46s} ║")
    print(f"  ╚{'═' * 48}╝")

    print(f"\n  Category: {meal.get('strCategory', 'N/A')}")
    print(f"  Cuisine:  {meal.get('strArea', 'N/A')}")

    # Extract ingredients (they're in strIngredient1 through strIngredient20)
    print(f"\n  INGREDIENTS:")
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}", "").strip()
        measure = meal.get(f"strMeasure{i}", "").strip()
        if ingredient:
            print(f"    - {measure} {ingredient}")

    # Instructions
    instructions = meal.get("strInstructions", "No instructions available.")
    print(f"\n  INSTRUCTIONS:")
    # Split into numbered steps
    steps = instructions.split("\r\n")
    step_num = 1
    for step in steps:
        step = step.strip()
        if step:
            print(f"    {step_num}. {step}")
            step_num += 1

    # Video link if available
    video = meal.get("strYoutube")
    if video:
        print(f"\n  Video tutorial: {video}")


# --- Main program ---
print("=== RECIPE FINDER ===")
print("  Find delicious recipes from around the world!\n")

while True:
    print("  1. Search by name")
    print("  2. Random recipe")
    print("  3. Browse categories")
    print("  4. Quit")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        query = input("  Search for: ").strip()
        if query:
            print("  Searching...")
            results = search_by_name(query)
            if results:
                print(f"\n  Found {len(results)} recipe(s):")
                for i, meal in enumerate(results, 1):
                    print(f"    {i}. {meal['strMeal']} ({meal.get('strArea', '?')})")

                try:
                    pick = int(input("\n  View recipe # (0 to skip): "))
                    if 1 <= pick <= len(results):
                        display_recipe(results[pick - 1])
                except ValueError:
                    pass
            else:
                print("  No recipes found. Try a different search.")

    elif choice == "2":
        print("  Getting a random recipe...")
        meal = get_random_recipe()
        display_recipe(meal)

    elif choice == "3":
        categories = get_categories()
        if categories:
            print("\n  Categories:")
            for i, cat in enumerate(categories, 1):
                print(f"    {i}. {cat['strCategory']} ({cat.get('strCategoryDescription', '')[:50]}...)")

            try:
                pick = int(input("\n  View category #: "))
                if 1 <= pick <= len(categories):
                    cat_name = categories[pick - 1]["strCategory"]
                    meals = search_by_category(cat_name)
                    print(f"\n  {cat_name} recipes:")
                    for i, m in enumerate(meals[:10], 1):
                        print(f"    {i}. {m['strMeal']}")
            except ValueError:
                pass

    elif choice == "4":
        print("  Bon appetit! Goodbye!")
        break

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a "favorites" feature — save recipes you like
# to a JSON file and view them later.

# CHALLENGE 2: Add a "meal planner" — pick recipes for each day
# of the week and generate a shopping list (combine all ingredients).

# CHALLENGE 3: Filter by cuisine (Italian, Mexican, etc.) using
# the API's filter.php?a=Italian endpoint.

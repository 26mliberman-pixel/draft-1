"""
PROJECT 04: WEATHER APP
=========================
Get real weather data from the internet! Learn APIs.

WHAT YOU'LL LEARN:
- What an API is
- HTTP requests with the requests library
- Parsing JSON from the web
- Error handling for network requests

WHAT IS AN API?
Think of a restaurant: you (the customer) don't go to the kitchen.
You tell the WAITER what you want, and the waiter brings it.
An API is the waiter — it's the way you ask a server for data.

SETUP:
pip install requests

NOTE: This uses a free API that doesn't require a key (wttr.in).
"""

import requests
import json

# ============================================================
# LESSON: HTTP Requests
# ============================================================

# The internet runs on HTTP requests:
# GET    — "Give me data" (reading)
# POST   — "Here's new data" (creating)
# PUT    — "Update this data" (updating)
# DELETE — "Remove this data" (deleting)

# The `requests` library makes this easy:

# A simple GET request:
# response = requests.get("https://api.example.com/data")
# response.status_code  → 200 means success
# response.json()       → Parse the JSON response into a Python dict
# response.text         → The raw text response

# ============================================================
# LESSON: Status codes
# ============================================================

# 200 — OK (success!)
# 301 — Moved (the URL changed)
# 400 — Bad Request (you sent something wrong)
# 401 — Unauthorized (you need a key/login)
# 404 — Not Found (wrong URL)
# 500 — Server Error (their problem, not yours)

# ============================================================
# THE PROJECT: Weather App using wttr.in
# ============================================================

def get_weather(city):
    """Get weather data for a city using wttr.in API."""
    try:
        # wttr.in has a JSON API — just add ?format=j1
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"  Error: Got status code {response.status_code}")
            return None

        return response.json()

    except requests.exceptions.ConnectionError:
        print("  Error: Could not connect. Check your internet!")
        return None
    except requests.exceptions.Timeout:
        print("  Error: Request timed out. Try again.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  Error: {e}")
        return None


def display_weather(data):
    """Display weather information nicely."""
    if not data:
        return

    try:
        current = data["current_condition"][0]
        location = data["nearest_area"][0]

        city = location["areaName"][0]["value"]
        country = location["country"][0]["value"]
        temp_c = current["temp_C"]
        temp_f = current["temp_F"]
        feels_c = current["FeelsLikeC"]
        feels_f = current["FeelsLikeF"]
        humidity = current["humidity"]
        description = current["weatherDesc"][0]["value"]
        wind_speed = current["windspeedKmph"]
        wind_dir = current["winddir16Point"]

        print(f"\n  === Weather for {city}, {country} ===\n")
        print(f"  Condition:    {description}")
        print(f"  Temperature:  {temp_c}°C / {temp_f}°F")
        print(f"  Feels like:   {feels_c}°C / {feels_f}°F")
        print(f"  Humidity:     {humidity}%")
        print(f"  Wind:         {wind_speed} km/h {wind_dir}")

        # 3-day forecast
        if "weather" in data:
            print(f"\n  === 3-Day Forecast ===\n")
            for day in data["weather"][:3]:
                date = day["date"]
                max_c = day["maxtempC"]
                min_c = day["mintempC"]
                desc = day["hourly"][4]["weatherDesc"][0]["value"]  # Noon weather
                print(f"  {date}: {min_c}°C – {max_c}°C, {desc}")

    except (KeyError, IndexError) as e:
        print(f"  Error parsing weather data: {e}")
        print("  The API response format may have changed.")


def get_simple_weather(city):
    """Get a simple one-line weather report."""
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"\n  {response.text.strip()}")
        else:
            print("  Could not get weather.")
    except requests.exceptions.RequestException:
        print("  Connection error.")


# --- Main program ---
print("=== WEATHER APP ===")
print("  Get weather for any city in the world!\n")

while True:
    print("  1. Detailed weather")
    print("  2. Quick weather (one line)")
    print("  3. Compare two cities")
    print("  4. Quit")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        city = input("  City name: ").strip()
        if city:
            print("  Fetching weather...")
            data = get_weather(city)
            display_weather(data)

    elif choice == "2":
        city = input("  City name: ").strip()
        if city:
            get_simple_weather(city)

    elif choice == "3":
        city1 = input("  First city: ").strip()
        city2 = input("  Second city: ").strip()
        if city1 and city2:
            print(f"\n  Comparing weather...")
            data1 = get_weather(city1)
            data2 = get_weather(city2)
            display_weather(data1)
            display_weather(data2)

    elif choice == "4":
        print("  Stay dry! Goodbye!")
        break

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Save weather history to a file. Every time you check
# weather, log the city, date, and temperature.

# CHALLENGE 2: Add weather alerts — if temp > 35°C, say "Heat warning!"
# If wind > 50 km/h, say "Wind warning!" etc.

# CHALLENGE 3: Show weather in a more visual way using ASCII art:
# ☀️ for sunny, 🌧️ for rain, ❄️ for snow, etc.

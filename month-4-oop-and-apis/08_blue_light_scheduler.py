"""
PROJECT 08: BLUE LIGHT SCHEDULER
==================================
"Make my phone have no blue light when it gets dark."

Your phone can't be controlled by Python, but the LOGIC behind the
"Night Light" / "Night Shift" feature is something you can build yourself!

The idea: screens emit blue light, which tricks your brain into thinking
it's daytime. At night that can hurt your sleep. So phones gradually remove
blue light (warm the screen to orange) from sunset to sunrise.

This program figures out, for YOUR location, exactly when blue light should
be reduced — by asking a real API for today's sunset and sunrise times.

WHAT YOU'LL LEARN:
- Calling a real, free API (no key needed)
- Working with dates and times (the datetime module)
- Turning real-world data into a simple schedule
- A tiny bit of math to ramp a value up and down

WHAT IS THIS API?
sunrise-sunset.org gives you the sunrise/sunset times for any latitude and
longitude on Earth. It's free and needs no sign-up.

SETUP:
pip install requests
"""

import requests
from datetime import datetime, timezone

# ============================================================
# LESSON: Why blue light matters
# ============================================================

# Light has a "color temperature" measured in Kelvin (K):
#   ~6500 K = cool, bluish daylight  (lots of blue light)
#   ~2700 K = warm, orange candlelight (almost no blue light)
#
# Night mode slowly shifts your screen from cool to warm after sunset.
# We'll calculate a "warmth" value (0% = full blue, 100% = no blue).


def get_sun_times(latitude, longitude):
    """Ask the API for today's sunrise and sunset (in UTC)."""
    try:
        url = "https://api.sunrise-sunset.org/json"
        # formatted=0 means we get machine-readable ISO times, not "7:32 AM"
        params = {"lat": latitude, "lng": longitude, "formatted": 0}
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            print(f"  Error: Got status code {response.status_code}")
            return None

        data = response.json()
        if data.get("status") != "OK":
            print(f"  Error: API said '{data.get('status')}'")
            return None

        return data["results"]

    except requests.exceptions.ConnectionError:
        print("  Error: Could not connect. Check your internet!")
        return None
    except requests.exceptions.Timeout:
        print("  Error: Request timed out. Try again.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  Error: {e}")
        return None


def parse_time(iso_string):
    """Turn an ISO time string from the API into a datetime object."""
    # The API returns times like "2026-05-22T19:41:00+00:00"
    return datetime.fromisoformat(iso_string)


def screen_warmth(now, sunset, sunrise):
    """
    Return how warm the screen should be RIGHT NOW, as a percentage.
      0%   = full daylight, all blue light on
      100% = night mode, blue light removed
    Between sunset and sunrise we return 100%. We also ramp gradually
    over a 30-minute "twilight" window so the change isn't jarring.
    """
    # If sunset is after sunrise in our numbers, it means sunset belongs
    # to "tonight" while sunrise is "tomorrow morning". For a simple demo
    # we compare against today's values and treat after-sunset as night.
    if sunset <= now or now <= sunrise:
        return 100  # it's dark → no blue light

    # How long until sunset, in minutes?
    minutes_to_sunset = (sunset - now).total_seconds() / 60

    # Start warming the screen 30 minutes BEFORE sunset.
    if minutes_to_sunset <= 30:
        # 30 min before = 0%, at sunset = 100%
        ramp = (30 - minutes_to_sunset) / 30 * 100
        return round(ramp)

    return 0  # full daylight, lots of blue light


def warmth_bar(percent):
    """Draw a little text bar so you can SEE the warmth level."""
    filled = round(percent / 10)
    return "[" + "#" * filled + "-" * (10 - filled) + f"] {percent}%"


# --- Main program ---
print("=== BLUE LIGHT SCHEDULER ===")
print("  Find out when your screen should drop blue light.\n")

# Some example locations so you can try it without looking anything up.
# (latitude, longitude) — north/east are positive, south/west are negative.
PRESETS = {
    "1": ("New York",  40.7128,  -74.0060),
    "2": ("London",    51.5074,   -0.1278),
    "3": ("Tokyo",     35.6762,  139.6503),
    "4": ("Sydney",   -33.8688,  151.2093),
}

print("  Pick a city, or enter your own coordinates:")
for key, (name, _, _) in PRESETS.items():
    print(f"  {key}. {name}")
print("  5. Enter my own latitude/longitude")

choice = input("\n  Choice: ").strip()

if choice in PRESETS:
    city, lat, lng = PRESETS[choice]
elif choice == "5":
    city = input("  Name this place: ").strip() or "your location"
    lat = float(input("  Latitude:  ").strip())
    lng = float(input("  Longitude: ").strip())
else:
    print("  Not a valid choice. Using New York.")
    city, lat, lng = PRESETS["1"]

print(f"\n  Looking up the sun for {city}...")
results = get_sun_times(lat, lng)

if results:
    sunset = parse_time(results["sunset"])
    sunrise = parse_time(results["sunrise"])
    now = datetime.now(timezone.utc)

    # Times come back in UTC. We show them in UTC to keep things simple —
    # CHALLENGE 1 below asks you to convert to local time.
    print(f"\n  Today in {city} (all times UTC):")
    print(f"    Sunrise: {sunrise.strftime('%H:%M')}")
    print(f"    Sunset:  {sunset.strftime('%H:%M')}")

    warmth = screen_warmth(now, sunset, sunrise)
    print(f"\n  Right now ({now.strftime('%H:%M')} UTC) your screen should be:")
    print(f"    {warmth_bar(warmth)} warm")

    if warmth == 0:
        print("    It's daytime — full screen, blue light is fine.")
    elif warmth == 100:
        print("    It's dark — blue light OFF for better sleep.")
    else:
        print("    Sunset is near — easing the blue light down...")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: The API gives UTC times. Convert sunset/sunrise to the
# user's LOCAL time so the schedule makes sense for them.
# Hint: look up "datetime astimezone" and the "zoneinfo" module.

# CHALLENGE 2: Print a full 24-hour table: for every hour from 00:00 to
# 23:00, show the warmth bar. You'll see it ramp up at sunset and back
# down at sunrise.

# CHALLENGE 3: Map the warmth percentage to an actual color temperature
# in Kelvin (0% = 6500K, 100% = 2700K) and print that number too.

# CHALLENGE 4: Save each day's sunrise/sunset to a file so you build a
# history, then find which day had the longest daylight.

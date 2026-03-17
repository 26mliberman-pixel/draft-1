"""
PROJECT 07: LOG ANALYZER
===========================
Analyze a log file — a realistic file processing task.

WHAT YOU'LL LEARN:
- Processing large text files line by line
- Regular patterns in real data
- Aggregating and summarizing data
- Tuples (immutable lists)
"""

# ============================================================
# LESSON: Tuples
# ============================================================

# A tuple is like a list, but you CAN'T change it after creation.
# Use parentheses () instead of square brackets [].

point = (10, 20)       # A coordinate
rgb = (255, 128, 0)    # A color

print(point[0])  # 10
print(point[1])  # 20

# Tuples are used for data that shouldn't change.
# They're also used when functions return multiple values.

# Tuple unpacking:
x, y = point
print(x)  # 10
print(y)  # 20

# You CAN'T do this with tuples:
# point[0] = 30  ← ERROR! Tuples are immutable.

# ============================================================
# Step 1: Create a sample log file
# ============================================================

import random
from datetime import datetime, timedelta

def generate_sample_log():
    """Create a realistic-looking web server log file."""
    pages = ["/", "/about", "/contact", "/products", "/login",
             "/dashboard", "/api/users", "/api/data", "/settings", "/404"]
    status_codes = [200, 200, 200, 200, 301, 404, 404, 500, 403, 200]
    ips = ["192.168.1." + str(random.randint(1, 50)) for _ in range(20)]

    lines = []
    start_time = datetime(2026, 3, 1, 0, 0, 0)

    for i in range(500):
        timestamp = start_time + timedelta(
            minutes=random.randint(0, 43200)  # 30 days of minutes
        )
        ip = random.choice(ips)
        page = random.choice(pages)
        status = random.choice(status_codes)
        size = random.randint(200, 50000)

        line = f'{ip} - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S")}] "GET {page} HTTP/1.1" {status} {size}'
        lines.append(line)

    lines.sort()  # Sort by IP (roughly chronological within each IP)

    with open("server.log", "w") as f:
        for line in lines:
            f.write(line + "\n")

    print(f"  Generated server.log with {len(lines)} entries.")


# ============================================================
# Step 2: The Log Analyzer
# ============================================================

def parse_log_line(line):
    """Parse a single log line into its components."""
    parts = line.split()
    if len(parts) < 9:
        return None

    ip = parts[0]
    # Extract date from [dd/Mon/YYYY:HH:MM:SS]
    date_str = parts[3].strip("[")
    page = parts[6]
    status = int(parts[8])
    size = int(parts[9]) if parts[9].isdigit() else 0

    return {
        "ip": ip,
        "date": date_str,
        "page": page,
        "status": status,
        "size": size
    }


def analyze_log(filename):
    """Analyze the log file and print a report."""
    entries = []

    with open(filename, "r") as f:
        for line in f:
            parsed = parse_log_line(line.strip())
            if parsed:
                entries.append(parsed)

    print(f"\n  === LOG ANALYSIS REPORT ===")
    print(f"  Total requests: {len(entries)}\n")

    # --- Most visited pages ---
    page_counts = {}
    for e in entries:
        page = e["page"]
        page_counts[page] = page_counts.get(page, 0) + 1

    print("  TOP PAGES:")
    sorted_pages = sorted(page_counts.items(), key=lambda x: x[1], reverse=True)
    for page, count in sorted_pages[:5]:
        bar = "#" * (count // 5)
        print(f"    {page:<20} {count:>5} hits  {bar}")

    # --- Status code breakdown ---
    status_counts = {}
    for e in entries:
        s = e["status"]
        status_counts[s] = status_counts.get(s, 0) + 1

    print(f"\n  STATUS CODES:")
    for status, count in sorted(status_counts.items()):
        label = {200: "OK", 301: "Redirect", 403: "Forbidden",
                 404: "Not Found", 500: "Server Error"}.get(status, "Other")
        print(f"    {status} ({label}): {count}")

    # --- Top IP addresses ---
    ip_counts = {}
    for e in entries:
        ip = e["ip"]
        ip_counts[ip] = ip_counts.get(ip, 0) + 1

    print(f"\n  TOP IPs (possible bots?):")
    sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
    for ip, count in sorted_ips[:5]:
        print(f"    {ip:<20} {count} requests")

    # --- 404 errors ---
    not_found = [e["page"] for e in entries if e["status"] == 404]
    if not_found:
        nf_counts = {}
        for page in not_found:
            nf_counts[page] = nf_counts.get(page, 0) + 1

        print(f"\n  404 ERRORS ({len(not_found)} total):")
        for page, count in sorted(nf_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"    {page}: {count} times")

    # --- Total bandwidth ---
    total_bytes = sum(e["size"] for e in entries)
    print(f"\n  BANDWIDTH: {total_bytes:,} bytes ({total_bytes / 1024 / 1024:.1f} MB)")


# --- Main program ---
print("=== LOG ANALYZER ===\n")
generate_sample_log()
analyze_log("server.log")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add time-based analysis — which hour of the day
# has the most traffic?

# CHALLENGE 2: Detect potential attacks — IPs with many 403/404
# errors in a short time.

# CHALLENGE 3: Export the report to a file (report.txt) in addition
# to printing it.

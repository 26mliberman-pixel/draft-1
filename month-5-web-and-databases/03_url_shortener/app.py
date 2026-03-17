"""
PROJECT 03: URL SHORTENER
============================
Like bit.ly — shorten long URLs! Learn DATABASES with SQLite.

WHAT YOU'LL LEARN:
- SQLite — a simple database
- SQL basics (CREATE, INSERT, SELECT)
- HTML forms with POST requests
- Redirects

WHAT IS A DATABASE?
A database is organized, persistent storage for data.
SQLite stores everything in a single file (no setup needed!).
SQL (Structured Query Language) is how you talk to it.
"""

from flask import Flask, render_template_string, request, redirect
import sqlite3
import random
import string

app = Flask(__name__)
DB_FILE = "urls.db"

# ============================================================
# LESSON: SQLite Basics
# ============================================================

def init_db():
    """Create the database table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # SQL to create a table:
    # CREATE TABLE table_name (
    #     column_name TYPE CONSTRAINTS,
    #     ...
    # )
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def generate_short_code(length=6):
    """Generate a random short code."""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def save_url(original_url, short_code):
    """Save a URL mapping to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # INSERT INTO table (columns) VALUES (values)
    cursor.execute(
        "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
        (short_code, original_url)
    )

    conn.commit()
    conn.close()


def get_url(short_code):
    """Look up the original URL for a short code."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # SELECT columns FROM table WHERE condition
    cursor.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    )
    result = cursor.fetchone()

    if result:
        # Update click count
        cursor.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
            (short_code,)
        )
        conn.commit()

    conn.close()
    return result[0] if result else None


def get_all_urls():
    """Get all shortened URLs."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT short_code, original_url, clicks, created_at FROM urls ORDER BY created_at DESC")
    results = cursor.fetchall()
    conn.close()
    return results


# ============================================================
# Flask Routes
# ============================================================

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>URL Shortener</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        .card { background: white; padding: 25px; border-radius: 10px; margin: 20px 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        input[type="url"] { width: 70%; padding: 10px; font-size: 16px; border: 1px solid #ddd;
                            border-radius: 5px; }
        button { padding: 10px 20px; background: #667eea; color: white; border: none;
                 border-radius: 5px; font-size: 16px; cursor: pointer; }
        button:hover { background: #5a6fd6; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #667eea; color: white; }
        a { color: #667eea; }
        .result { background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 15px 0;
                  font-size: 1.2em; }
        .error { background: #ffebee; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>URL Shortener</h1>

    <div class="card">
        <h2>Shorten a URL</h2>
        <form method="POST" action="/shorten">
            <input type="url" name="url" placeholder="https://example.com/very/long/url" required>
            <button type="submit">Shorten!</button>
        </form>

        {% if short_url %}
        <div class="result">
            Short URL: <a href="{{ short_url }}">{{ short_url }}</a>
        </div>
        {% endif %}

        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>

    <div class="card">
        <h2>All Shortened URLs ({{ urls|length }})</h2>
        {% if urls %}
        <table>
            <tr>
                <th>Short Code</th>
                <th>Original URL</th>
                <th>Clicks</th>
                <th>Created</th>
            </tr>
            {% for url in urls %}
            <tr>
                <td><a href="/{{ url[0] }}">{{ url[0] }}</a></td>
                <td>{{ url[1][:50] }}{% if url[1]|length > 50 %}...{% endif %}</td>
                <td>{{ url[2] }}</td>
                <td>{{ url[3][:10] }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No URLs shortened yet. Try it above!</p>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    urls = get_all_urls()
    return render_template_string(TEMPLATE, urls=urls, short_url=None, error=None)


@app.route("/shorten", methods=["POST"])
def shorten():
    original_url = request.form.get("url", "").strip()

    if not original_url:
        urls = get_all_urls()
        return render_template_string(TEMPLATE, urls=urls, short_url=None,
                                       error="Please enter a URL!")

    # Add https:// if missing
    if not original_url.startswith(("http://", "https://")):
        original_url = "https://" + original_url

    short_code = generate_short_code()
    try:
        save_url(original_url, short_code)
    except sqlite3.IntegrityError:
        short_code = generate_short_code(8)  # Try a longer code
        save_url(original_url, short_code)

    short_url = request.host_url + short_code
    urls = get_all_urls()
    return render_template_string(TEMPLATE, urls=urls, short_url=short_url, error=None)


@app.route("/<short_code>")
def redirect_url(short_code):
    """Redirect short URL to original URL."""
    original = get_url(short_code)
    if original:
        return redirect(original)
    return "URL not found!", 404


# Initialize database and run
init_db()

if __name__ == "__main__":
    print("\n  URL Shortener running!")
    print("  Open http://127.0.0.1:5000\n")
    app.run(debug=True)

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Let users choose their own custom short code
# (e.g., "mysite" → yoururl.com/mysite).

# CHALLENGE 2: Add a statistics page for each URL showing
# click count over time.

# CHALLENGE 3: Add URL validation — check if the URL actually exists
# before shortening it (use requests.head()).

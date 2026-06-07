"""
CAPSTONE 04: RESALE APPRECIATION ANALYZER
==========================================
"Which item should I buy from the catalog to resell for the biggest profit?"

This app keeps a catalog of items you can buy (sneakers, watches, trading
cards, consoles, handbags...), records what each one costs to buy and what it
currently resells for, and then RANKS them so you can see — at a glance — which
item has appreciated the most. The #1 pick is the "best buy to flip".

SKILLS USED:
- Flask (Month 5)            -> the web interface
- SQLite databases (Month 5) -> storing the catalog
- Functions & control flow (Month 2)
- Lists, dicts, sorting (Month 3)
- The basics: math, strings, formatting (Month 1)

SETUP:
  pip install flask
  python app.py
  Then open http://127.0.0.1:5000

KEY IDEA — "appreciation":
  Appreciation is how much an item GAINED in value, as a percentage.

      appreciation % = (resale_price - buy_price) / buy_price * 100

  Example: buy a sneaker for $200, it now resells for $350.
      (350 - 200) / 200 * 100 = 75%   -> it appreciated 75%

  Because flipping takes time, we ALSO show the *annualized* appreciation
  (how fast it grows per year), so a 30% gain in 3 months beats a 30% gain
  over 2 years. That is the fairest way to compare "highest appreciation".

FEATURES:
  1. Add items to the catalog (buy price, resale price, hold time)
  2. See the single BEST item to buy & resell (highest annualized appreciation)
  3. Browse the full catalog ranked best-to-worst
  4. Filter by category
  5. Delete items
  6. Auto-seeds with realistic example data on first run
"""

from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)
DB_FILE = "resale.db"

CATEGORIES = [
    "Sneakers", "Watches", "Trading Cards", "Consoles",
    "Handbags", "Lego Sets", "Vinyl Records", "Other",
]


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            buy_price REAL NOT NULL,
            resale_price REAL NOT NULL,
            months_held REAL NOT NULL DEFAULT 12,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Seed with example data the very first time, so the app isn't empty.
    count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    if count == 0:
        seed = [
            # (name, category, buy_price, resale_price, months_held)
            ("Nike Dunk Low Panda",        "Sneakers",      115, 180, 6),
            ("Jordan 1 Retro Chicago",     "Sneakers",      180, 430, 18),
            ("Pokemon Charizard (PSA 9)",  "Trading Cards", 250, 900, 24),
            ("Rolex Oyster Perpetual",     "Watches",      5800, 7200, 12),
            ("PlayStation 5 (launch)",     "Consoles",      500, 640, 4),
            ("Lego Millennium Falcon",     "Lego Sets",     800, 1100, 30),
            ("Louis Vuitton Neverfull",    "Handbags",     1500, 1750, 12),
            ("Taylor Swift 1989 Vinyl",    "Vinyl Records",  35, 95, 9),
        ]
        conn.executemany(
            "INSERT INTO items (name, category, buy_price, resale_price, months_held) "
            "VALUES (?, ?, ?, ?, ?)",
            seed,
        )
        conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# The maths: appreciation & annualized appreciation
# ---------------------------------------------------------------------------
def appreciation_pct(buy_price, resale_price):
    """Total percentage gain (or loss) from buy price to resale price."""
    if buy_price <= 0:
        return 0.0
    return (resale_price - buy_price) / buy_price * 100


def annualized_pct(buy_price, resale_price, months_held):
    """
    How fast the value grows PER YEAR, so items held for different lengths
    of time can be compared fairly. Uses simple compound growth.
    """
    if buy_price <= 0 or months_held <= 0:
        return 0.0
    growth = resale_price / buy_price            # e.g. 1.75 means +75%
    years = months_held / 12
    return (growth ** (1 / years) - 1) * 100


def analyze(rows):
    """Turn raw DB rows into a list of dicts with the computed numbers,
    sorted from best (highest annualized appreciation) to worst."""
    items = []
    for r in rows:
        profit = r["resale_price"] - r["buy_price"]
        items.append({
            "id": r["id"],
            "name": r["name"],
            "category": r["category"],
            "buy_price": r["buy_price"],
            "resale_price": r["resale_price"],
            "months_held": r["months_held"],
            "profit": profit,
            "appreciation": appreciation_pct(r["buy_price"], r["resale_price"]),
            "annualized": annualized_pct(
                r["buy_price"], r["resale_price"], r["months_held"]
            ),
        })
    items.sort(key=lambda x: x["annualized"], reverse=True)
    return items


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
# A single self-contained template. (We keep everything in one string so the
# whole project is one file — no separate templates/ folder to manage.)
PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Resale Appreciation Analyzer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; color: #333; }
        nav { background: #1a2b4a; padding: 15px 30px; display: flex;
              justify-content: space-between; align-items: center; }
        nav h1 { color: white; font-size: 1.3em; }
        nav a { color: #b8c4d9; text-decoration: none; margin-left: 20px; }
        nav a:hover { color: white; }
        main { max-width: 1000px; margin: 30px auto; padding: 0 20px; }
        h2 { margin-bottom: 15px; color: #1a2b4a; }

        .best {
            background: linear-gradient(135deg, #11998e, #38ef7d);
            color: white; padding: 28px; border-radius: 12px; margin-bottom: 25px;
            box-shadow: 0 4px 18px rgba(17,153,142,0.3);
        }
        .best h3 { font-size: 0.95em; text-transform: uppercase; opacity: 0.9; }
        .best .name { font-size: 2em; font-weight: bold; margin: 6px 0; }
        .best .stats { display: flex; gap: 30px; margin-top: 12px; flex-wrap: wrap; }
        .best .stat b { display: block; font-size: 1.5em; }

        .card { background: white; padding: 25px; border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08); margin-bottom: 20px; }
        .two-col { display: grid; grid-template-columns: 1.4fr 1fr; gap: 20px; }

        .form-group { margin: 12px 0; }
        label { display: block; margin-bottom: 4px; font-weight: 600; font-size: 0.9em; }
        input, select { width: 100%; padding: 10px; border: 1px solid #ddd;
                        border-radius: 5px; font-size: 1em; }
        .btn { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;
               font-size: 1em; color: white; background: #1a2b4a; }

        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; color: #666; font-size: 0.8em; text-transform: uppercase; }
        .pos { color: #11998e; font-weight: bold; }
        .neg { color: #e74c3c; font-weight: bold; }
        .rank { color: #888; font-weight: bold; }
        .filters a { margin-right: 10px; font-size: 0.9em; text-decoration: none;
                     color: #1a2b4a; padding: 4px 10px; border-radius: 5px; background: #e8edf5; }
        .filters a.active { background: #1a2b4a; color: white; }
        .del { color: #e74c3c; text-decoration: none; }
    </style>
</head>
<body>
    <nav>
        <h1>📈 Resale Appreciation Analyzer</h1>
        <div><a href="/">Best Buys</a></div>
    </nav>
    <main>
    {% if best %}
    <div class="best">
        <h3>🏆 Best item to buy &amp; resell</h3>
        <div class="name">{{ best.name }}</div>
        <div>{{ best.category }} — buy at ${{ "%.0f"|format(best.buy_price) }},
             resells for ${{ "%.0f"|format(best.resale_price) }}</div>
        <div class="stats">
            <div class="stat"><b>{{ "%.1f"|format(best.annualized) }}%</b>per year</div>
            <div class="stat"><b>{{ "%.1f"|format(best.appreciation) }}%</b>total gain</div>
            <div class="stat"><b>${{ "%.0f"|format(best.profit) }}</b>profit / unit</div>
        </div>
    </div>
    {% endif %}

    <div class="two-col">
        <div class="card">
            <h2>Catalog — ranked by appreciation</h2>
            <div class="filters" style="margin-bottom:12px;">
                <a href="/" class="{{ 'active' if not active_cat }}">All</a>
                {% for c in categories %}
                <a href="/?category={{ c }}"
                   class="{{ 'active' if active_cat == c }}">{{ c }}</a>
                {% endfor %}
            </div>
            <table>
                <tr>
                    <th>#</th><th>Item</th><th>Buy</th><th>Resale</th>
                    <th>Held</th><th>Total</th><th>Per Year</th><th></th>
                </tr>
                {% for it in items %}
                <tr>
                    <td class="rank">{{ loop.index }}</td>
                    <td><b>{{ it.name }}</b><br>
                        <span style="color:#888;font-size:0.85em;">{{ it.category }}</span></td>
                    <td>${{ "%.0f"|format(it.buy_price) }}</td>
                    <td>${{ "%.0f"|format(it.resale_price) }}</td>
                    <td>{{ "%.0f"|format(it.months_held) }}mo</td>
                    <td class="{{ 'pos' if it.appreciation >= 0 else 'neg' }}">
                        {{ "%.1f"|format(it.appreciation) }}%</td>
                    <td class="{{ 'pos' if it.annualized >= 0 else 'neg' }}">
                        {{ "%.1f"|format(it.annualized) }}%</td>
                    <td><a class="del" href="/delete/{{ it.id }}"
                           onclick="return confirm('Delete?')">✕</a></td>
                </tr>
                {% endfor %}
                {% if not items %}
                <tr><td colspan="8" style="color:#888;">No items yet. Add one!</td></tr>
                {% endif %}
            </table>
        </div>

        <div class="card">
            <h2>Add an item</h2>
            <form method="POST" action="/add">
                <div class="form-group">
                    <label>Item name</label>
                    <input type="text" name="name" placeholder="e.g. Jordan 4 Bred" required>
                </div>
                <div class="form-group">
                    <label>Category</label>
                    <select name="category">
                        {% for c in categories %}<option>{{ c }}</option>{% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label>Buy price ($)</label>
                    <input type="number" name="buy_price" step="0.01" min="0.01" required>
                </div>
                <div class="form-group">
                    <label>Resale price ($)</label>
                    <input type="number" name="resale_price" step="0.01" min="0" required>
                </div>
                <div class="form-group">
                    <label>Months held before reselling</label>
                    <input type="number" name="months_held" step="0.5" min="0.5" value="12" required>
                </div>
                <button type="submit" class="btn">Add to catalog</button>
            </form>
        </div>
    </div>
    </main>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    active_cat = request.args.get("category", "")
    conn = get_db()
    if active_cat:
        rows = conn.execute(
            "SELECT * FROM items WHERE category = ?", (active_cat,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM items").fetchall()
    conn.close()

    items = analyze(rows)
    best = items[0] if items else None

    return render_template_string(
        PAGE,
        items=items,
        best=best,
        categories=CATEGORIES,
        active_cat=active_cat,
    )


@app.route("/add", methods=["POST"])
def add():
    try:
        buy = float(request.form["buy_price"])
        resale = float(request.form["resale_price"])
        months = float(request.form["months_held"])
    except (ValueError, KeyError):
        return redirect("/")

    conn = get_db()
    conn.execute(
        "INSERT INTO items (name, category, buy_price, resale_price, months_held) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            request.form["name"],
            request.form.get("category", "Other"),
            buy,
            resale,
            months,
        ),
    )
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/delete/<int:item_id>")
def delete(item_id):
    conn = get_db()
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect("/")


init_db()

if __name__ == "__main__":
    print("\n  Resale Appreciation Analyzer running!")
    print("  Open http://127.0.0.1:5000\n")
    app.run(debug=True)

"""
CAPSTONE 02: HABIT TRACKER
==============================
Track daily habits and visualize your streaks!

SKILLS USED: Everything from months 1-5.

SETUP: pip install flask

FEATURES:
- Add habits to track
- Check off daily completions
- View streaks and stats
- Calendar-style visualization
"""

from flask import Flask, render_template_string, request, redirect, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
DB_FILE = "habits.db"


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            color TEXT DEFAULT '#3498db',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id),
            UNIQUE(habit_id, date)
        )
    """)
    conn.commit()
    conn.close()


def get_streak(habit_id):
    """Calculate current streak for a habit."""
    conn = get_db()
    dates = conn.execute(
        "SELECT date FROM completions WHERE habit_id = ? ORDER BY date DESC",
        (habit_id,)
    ).fetchall()
    conn.close()

    if not dates:
        return 0

    streak = 0
    today = datetime.now().date()
    check_date = today

    date_set = {d["date"] for d in dates}

    # Check if today or yesterday is completed (grace period)
    if str(today) not in date_set:
        yesterday = today - timedelta(days=1)
        if str(yesterday) not in date_set:
            return 0
        check_date = yesterday

    while str(check_date) in date_set:
        streak += 1
        check_date -= timedelta(days=1)

    return streak


COLORS = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6",
          "#1abc9c", "#e67e22", "#34495e"]

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Habit Tracker</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee;
               min-height: 100vh; }

        header { background: #16213e; padding: 20px 30px; text-align: center; }
        header h1 { color: #e94560; }
        header p { color: #8888aa; margin-top: 5px; }

        main { max-width: 900px; margin: 30px auto; padding: 0 20px; }

        .card { background: #16213e; border-radius: 12px; padding: 25px;
                margin: 20px 0; }

        .today-header { display: flex; justify-content: space-between; align-items: center; }

        .habit-row {
            display: flex; align-items: center; padding: 15px;
            margin: 10px 0; background: #0f3460; border-radius: 8px;
            transition: transform 0.1s;
        }
        .habit-row:hover { transform: translateX(5px); }

        .habit-check {
            width: 35px; height: 35px; border-radius: 50%; border: 3px solid #555;
            margin-right: 15px; cursor: pointer; display: flex;
            align-items: center; justify-content: center; font-size: 1.2em;
            transition: all 0.2s;
        }
        .habit-check.done { border-color: #2ecc71; background: #2ecc71; }

        .habit-info { flex: 1; }
        .habit-info h3 { margin-bottom: 3px; }
        .habit-info .desc { color: #8888aa; font-size: 0.9em; }

        .streak { text-align: right; }
        .streak .number { font-size: 1.8em; font-weight: bold; }
        .streak .label { font-size: 0.8em; color: #8888aa; }

        /* Calendar grid */
        .calendar { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px;
                    margin: 15px 0; }
        .cal-day { width: 100%; aspect-ratio: 1; border-radius: 4px;
                   background: #0f3460; display: flex; align-items: center;
                   justify-content: center; font-size: 0.75em; color: #888; }
        .cal-day.done { background: var(--habit-color, #2ecc71); color: white; }
        .cal-day.today { border: 2px solid #e94560; }
        .cal-header { color: #666; font-size: 0.8em; text-align: center; padding: 5px; }

        /* Form */
        input, select { padding: 10px; border: 1px solid #333; background: #0f3460;
                        color: white; border-radius: 5px; font-size: 1em; width: 100%; }
        .form-row { display: flex; gap: 10px; margin: 10px 0; }
        .form-row > * { flex: 1; }

        .btn { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;
               font-size: 1em; color: white; background: #e94560; }
        .btn:hover { background: #c0392b; }

        .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        .stat-box { text-align: center; padding: 15px; background: #0f3460; border-radius: 8px; }
        .stat-box .num { font-size: 2em; font-weight: bold; color: #e94560; }
        .stat-box .label { font-size: 0.85em; color: #8888aa; }

        .delete-btn { color: #e74c3c; cursor: pointer; text-decoration: none;
                      font-size: 0.9em; margin-left: 10px; }
    </style>
</head>
<body>
    <header>
        <h1>Habit Tracker</h1>
        <p>{{ today_str }}</p>
    </header>

    <main>
        <!-- Today's Habits -->
        <div class="card">
            <div class="today-header">
                <h2>Today's Habits</h2>
                <span>{{ completed_today }}/{{ total_habits }} done</span>
            </div>

            {% for habit in habits %}
            <div class="habit-row">
                <div class="habit-check {{ 'done' if habit.done_today }}"
                     onclick="toggleHabit({{ habit.id }})"
                     style="border-color: {{ habit.color }}; {% if habit.done_today %}background: {{ habit.color }};{% endif %}">
                    {% if habit.done_today %}&#10003;{% endif %}
                </div>
                <div class="habit-info">
                    <h3>{{ habit.name }}</h3>
                    <div class="desc">{{ habit.description or '' }}</div>
                </div>
                <div class="streak">
                    <div class="number">{{ habit.streak }}</div>
                    <div class="label">day streak</div>
                </div>
            </div>
            {% endfor %}

            {% if not habits %}
            <p style="color: #888; padding: 20px;">No habits yet. Add one below!</p>
            {% endif %}
        </div>

        <!-- Add Habit -->
        <div class="card">
            <h2>Add New Habit</h2>
            <form method="POST" action="/add">
                <div class="form-row">
                    <input type="text" name="name" placeholder="Habit name (e.g., Exercise)" required>
                    <input type="text" name="description" placeholder="Description (optional)">
                </div>
                <div class="form-row">
                    <select name="color">
                        {% for color in colors %}
                        <option value="{{ color }}" style="background: {{ color }};">Color {{ loop.index }}</option>
                        {% endfor %}
                    </select>
                    <button type="submit" class="btn">Add Habit</button>
                </div>
            </form>
        </div>

        <!-- Stats -->
        {% if habits %}
        <div class="card">
            <h2>Stats</h2>
            <div class="stats">
                <div class="stat-box">
                    <div class="num">{{ total_completions }}</div>
                    <div class="label">Total Check-ins</div>
                </div>
                <div class="stat-box">
                    <div class="num">{{ best_streak }}</div>
                    <div class="label">Best Streak</div>
                </div>
                <div class="stat-box">
                    <div class="num">{{ completion_rate }}%</div>
                    <div class="label">This Week</div>
                </div>
            </div>
        </div>

        <!-- Manage -->
        <div class="card">
            <h2>Manage Habits</h2>
            {% for habit in habits %}
            <div style="display: flex; justify-content: space-between; padding: 8px 0;
                        border-bottom: 1px solid #333;">
                <span style="color: {{ habit.color }};">{{ habit.name }}</span>
                <a href="/delete/{{ habit.id }}" class="delete-btn"
                   onclick="return confirm('Delete this habit and all its data?');">Delete</a>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </main>

    <script>
        function toggleHabit(habitId) {
            fetch('/toggle/' + habitId, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                window.location.reload();
            });
        }
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    conn = get_db()
    today = datetime.now().strftime("%Y-%m-%d")

    habits_raw = conn.execute("SELECT * FROM habits ORDER BY created_at").fetchall()
    habits = []
    completed_today = 0

    for h in habits_raw:
        done = conn.execute(
            "SELECT 1 FROM completions WHERE habit_id = ? AND date = ?",
            (h["id"], today)
        ).fetchone() is not None

        streak = get_streak(h["id"])
        if done:
            completed_today += 1

        habits.append({
            "id": h["id"], "name": h["name"], "description": h["description"],
            "color": h["color"], "done_today": done, "streak": streak
        })

    total_completions = conn.execute("SELECT COUNT(*) FROM completions").fetchone()[0]
    best_streak = max((h["streak"] for h in habits), default=0)

    # This week's completion rate
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    week_completions = conn.execute(
        "SELECT COUNT(*) FROM completions WHERE date >= ?", (week_ago,)
    ).fetchone()[0]
    possible = len(habits) * 7
    completion_rate = round(week_completions / possible * 100) if possible > 0 else 0

    conn.close()

    return render_template_string(
        TEMPLATE,
        habits=habits,
        total_habits=len(habits),
        completed_today=completed_today,
        today_str=datetime.now().strftime("%A, %B %d, %Y"),
        colors=COLORS,
        total_completions=total_completions,
        best_streak=best_streak,
        completion_rate=completion_rate,
    )


@app.route("/add", methods=["POST"])
def add_habit():
    conn = get_db()
    conn.execute(
        "INSERT INTO habits (name, description, color) VALUES (?, ?, ?)",
        (request.form["name"], request.form.get("description", ""), request.form.get("color", "#3498db"))
    )
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/toggle/<int:habit_id>", methods=["POST"])
def toggle_habit(habit_id):
    conn = get_db()
    today = datetime.now().strftime("%Y-%m-%d")

    existing = conn.execute(
        "SELECT 1 FROM completions WHERE habit_id = ? AND date = ?",
        (habit_id, today)
    ).fetchone()

    if existing:
        conn.execute(
            "DELETE FROM completions WHERE habit_id = ? AND date = ?",
            (habit_id, today)
        )
    else:
        conn.execute(
            "INSERT INTO completions (habit_id, date) VALUES (?, ?)",
            (habit_id, today)
        )

    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@app.route("/delete/<int:habit_id>")
def delete_habit(habit_id):
    conn = get_db()
    conn.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
    conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()
    return redirect("/")


init_db()

if __name__ == "__main__":
    print("\n  Habit Tracker running!")
    print("  Open http://127.0.0.1:5000\n")
    app.run(debug=True)

"""
CAPSTONE 01: PERSONAL FINANCE DASHBOARD
==========================================
A full-featured finance tracker with a web interface.

SKILLS USED:
- Flask (Month 5)
- SQLite databases (Month 5)
- Classes and OOP (Month 4)
- File I/O and JSON (Month 3)
- Functions and control flow (Month 2)
- All the basics (Month 1)

SETUP:
  pip install flask

FEATURES:
- Add income and expenses
- View transactions with filters
- Dashboard with spending summary
- Category breakdown
- Monthly trends
"""

from flask import Flask, render_template_string, request, redirect, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
DB_FILE = "finance.db"


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE NOT NULL,
            monthly_limit REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


EXPENSE_CATEGORIES = [
    "Food", "Transport", "Housing", "Entertainment",
    "Shopping", "Health", "Education", "Bills", "Other"
]

INCOME_CATEGORIES = ["Salary", "Freelance", "Investments", "Gifts", "Other"]

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Finance Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; color: #333; }

        nav { background: #2c3e50; padding: 15px 30px; display: flex;
              justify-content: space-between; align-items: center; }
        nav h1 { color: white; font-size: 1.4em; }
        nav a { color: #bdc3c7; text-decoration: none; margin-left: 20px; }
        nav a:hover { color: white; }

        main { max-width: 1000px; margin: 30px auto; padding: 0 20px; }

        .summary-cards {
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: white; padding: 25px; border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        .card h3 { color: #888; font-size: 0.9em; text-transform: uppercase; }
        .card .amount { font-size: 2em; font-weight: bold; margin: 10px 0; }
        .card .income { color: #27ae60; }
        .card .expense { color: #e74c3c; }
        .card .balance { color: #2c3e50; }

        .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

        h2 { margin-bottom: 15px; color: #2c3e50; }

        /* Form */
        .form-group { margin: 12px 0; }
        label { display: block; margin-bottom: 4px; font-weight: 600; font-size: 0.9em; }
        input, select { width: 100%; padding: 10px; border: 1px solid #ddd;
                        border-radius: 5px; font-size: 1em; }
        .btn { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;
               font-size: 1em; color: white; }
        .btn-primary { background: #3498db; }
        .btn-success { background: #27ae60; }
        .btn-danger { background: #e74c3c; }

        /* Table */
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; color: #666; font-size: 0.85em; text-transform: uppercase; }
        .type-income { color: #27ae60; font-weight: bold; }
        .type-expense { color: #e74c3c; font-weight: bold; }

        /* Category bars */
        .cat-bar-container { margin: 8px 0; }
        .cat-bar-label { display: flex; justify-content: space-between; font-size: 0.9em; }
        .cat-bar { height: 12px; background: #eee; border-radius: 6px; overflow: hidden; }
        .cat-bar-fill { height: 100%; border-radius: 6px; }

        .tab-buttons { margin-bottom: 15px; }
        .tab-buttons button { padding: 8px 16px; border: 1px solid #ddd; background: white;
                              cursor: pointer; border-radius: 5px; margin-right: 5px; }
        .tab-buttons button.active { background: #3498db; color: white; border-color: #3498db; }
    </style>
</head>
<body>
    <nav>
        <h1>Finance Dashboard</h1>
        <div>
            <a href="/">Dashboard</a>
            <a href="/transactions">All Transactions</a>
        </div>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
{% extends base %}
{% block content %}
    <div class="summary-cards">
        <div class="card">
            <h3>Total Income</h3>
            <div class="amount income">${{ "%.2f"|format(total_income) }}</div>
        </div>
        <div class="card">
            <h3>Total Expenses</h3>
            <div class="amount expense">${{ "%.2f"|format(total_expenses) }}</div>
        </div>
        <div class="card">
            <h3>Balance</h3>
            <div class="amount balance">${{ "%.2f"|format(total_income - total_expenses) }}</div>
        </div>
    </div>

    <div class="two-col">
        <div class="card">
            <h2>Add Transaction</h2>
            <form method="POST" action="/add">
                <div class="form-group">
                    <label>Type</label>
                    <select name="type" id="type-select" onchange="updateCategories()">
                        <option value="expense">Expense</option>
                        <option value="income">Income</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Amount ($)</label>
                    <input type="number" name="amount" step="0.01" min="0.01" required>
                </div>
                <div class="form-group">
                    <label>Category</label>
                    <select name="category" id="category-select">
                        {% for cat in expense_categories %}
                        <option value="{{ cat }}">{{ cat }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <input type="text" name="description" placeholder="What was this for?">
                </div>
                <div class="form-group">
                    <label>Date</label>
                    <input type="date" name="date" value="{{ today }}">
                </div>
                <button type="submit" class="btn btn-primary">Add Transaction</button>
            </form>
        </div>

        <div class="card">
            <h2>Spending by Category</h2>
            {% for cat in categories %}
            <div class="cat-bar-container">
                <div class="cat-bar-label">
                    <span>{{ cat.name }}</span>
                    <span>${{ "%.2f"|format(cat.amount) }}</span>
                </div>
                <div class="cat-bar">
                    <div class="cat-bar-fill" style="width: {{ cat.percentage }}%;
                         background: hsl({{ loop.index * 40 }}, 70%, 55%);"></div>
                </div>
            </div>
            {% endfor %}
            {% if not categories %}
            <p style="color: #888;">No expenses yet.</p>
            {% endif %}
        </div>
    </div>

    <div class="card" style="margin-top: 20px;">
        <h2>Recent Transactions</h2>
        <table>
            <tr>
                <th>Date</th><th>Type</th><th>Category</th>
                <th>Description</th><th>Amount</th><th></th>
            </tr>
            {% for t in recent %}
            <tr>
                <td>{{ t.date }}</td>
                <td class="type-{{ t.type }}">{{ t.type }}</td>
                <td>{{ t.category }}</td>
                <td>{{ t.description or '-' }}</td>
                <td>${{ "%.2f"|format(t.amount) }}</td>
                <td><a href="/delete/{{ t.id }}" onclick="return confirm('Delete?')"
                       style="color: #e74c3c; text-decoration: none;">x</a></td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <script>
        const expenseCats = {{ expense_categories | tojson }};
        const incomeCats = {{ income_categories | tojson }};

        function updateCategories() {
            const type = document.getElementById('type-select').value;
            const select = document.getElementById('category-select');
            const cats = type === 'income' ? incomeCats : expenseCats;

            select.innerHTML = '';
            cats.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                select.appendChild(option);
            });
        }
    </script>
{% endblock %}
"""


@app.route("/")
def dashboard():
    conn = get_db()

    total_income = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'income'"
    ).fetchone()[0]

    total_expenses = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'expense'"
    ).fetchone()[0]

    # Category breakdown
    cat_data = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM transactions WHERE type = 'expense'
        GROUP BY category ORDER BY total DESC
    """).fetchall()

    categories = []
    for c in cat_data:
        pct = (c["total"] / total_expenses * 100) if total_expenses > 0 else 0
        categories.append({"name": c["category"], "amount": c["total"], "percentage": pct})

    recent = conn.execute(
        "SELECT * FROM transactions ORDER BY date DESC, id DESC LIMIT 10"
    ).fetchall()

    conn.close()

    return render_template_string(
        DASHBOARD_TEMPLATE,
        base=TEMPLATE,
        total_income=total_income,
        total_expenses=total_expenses,
        categories=categories,
        recent=recent,
        today=datetime.now().strftime("%Y-%m-%d"),
        expense_categories=EXPENSE_CATEGORIES,
        income_categories=INCOME_CATEGORIES,
    )


@app.route("/add", methods=["POST"])
def add_transaction():
    conn = get_db()
    conn.execute(
        "INSERT INTO transactions (type, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
        (
            request.form["type"],
            float(request.form["amount"]),
            request.form["category"],
            request.form.get("description", ""),
            request.form["date"],
        )
    )
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/delete/<int:tid>")
def delete_transaction(tid):
    conn = get_db()
    conn.execute("DELETE FROM transactions WHERE id = ?", (tid,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/transactions")
def all_transactions():
    conn = get_db()
    transactions = conn.execute(
        "SELECT * FROM transactions ORDER BY date DESC, id DESC"
    ).fetchall()
    conn.close()

    html = """
    {% extends base %}
    {% block content %}
    <div class="card">
        <h2>All Transactions ({{ transactions|length }})</h2>
        <table>
            <tr><th>Date</th><th>Type</th><th>Category</th><th>Description</th><th>Amount</th><th></th></tr>
            {% for t in transactions %}
            <tr>
                <td>{{ t.date }}</td>
                <td class="type-{{ t.type }}">{{ t.type }}</td>
                <td>{{ t.category }}</td>
                <td>{{ t.description or '-' }}</td>
                <td>${{ "%.2f"|format(t.amount) }}</td>
                <td><a href="/delete/{{ t.id }}" onclick="return confirm('Delete?')" style="color:#e74c3c;">x</a></td>
            </tr>
            {% endfor %}
        </table>
    </div>
    {% endblock %}
    """
    return render_template_string(html, base=TEMPLATE, transactions=transactions)


init_db()

if __name__ == "__main__":
    print("\n  Finance Dashboard running!")
    print("  Open http://127.0.0.1:5000\n")
    app.run(debug=True)

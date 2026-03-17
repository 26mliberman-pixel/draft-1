"""
PROJECT 05: REST API
======================
Build an API that other programs can use.

WHAT YOU'LL LEARN:
- What REST is
- Building API endpoints
- Returning JSON
- HTTP methods (GET, POST, PUT, DELETE)
- Testing APIs

WHAT IS A REST API?
A REST API is a set of URLs that programs (not humans) use to exchange data.
Instead of returning HTML pages, they return JSON data.

For example:
  GET    /api/books     → Get all books
  GET    /api/books/1   → Get book #1
  POST   /api/books     → Create a new book
  PUT    /api/books/1   → Update book #1
  DELETE /api/books/1   → Delete book #1
"""

from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB_FILE = "books_api.db"


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            rating REAL DEFAULT 0
        )
    """)

    # Add sample data if empty
    count = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    if count == 0:
        sample_books = [
            ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Fiction", 4.2),
            ("To Kill a Mockingbird", "Harper Lee", 1960, "Fiction", 4.5),
            ("1984", "George Orwell", 1949, "Dystopian", 4.4),
            ("Python Crash Course", "Eric Matthes", 2019, "Programming", 4.7),
            ("Clean Code", "Robert C. Martin", 2008, "Programming", 4.3),
        ]
        conn.executemany(
            "INSERT INTO books (title, author, year, genre, rating) VALUES (?, ?, ?, ?, ?)",
            sample_books
        )

    conn.commit()
    conn.close()


# ============================================================
# API ENDPOINTS
# ============================================================

@app.route("/")
def home():
    """API documentation page."""
    return """
    <html>
    <head><title>Books API</title>
    <style>
        body { font-family: monospace; max-width: 800px; margin: 50px auto; padding: 20px; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #333; color: white; }
    </style>
    </head>
    <body>
        <h1>Books API</h1>
        <p>A REST API for managing books.</p>
        <table>
            <tr><th>Method</th><th>Endpoint</th><th>Description</th></tr>
            <tr><td>GET</td><td><code>/api/books</code></td><td>Get all books</td></tr>
            <tr><td>GET</td><td><code>/api/books/1</code></td><td>Get book by ID</td></tr>
            <tr><td>POST</td><td><code>/api/books</code></td><td>Create a book</td></tr>
            <tr><td>PUT</td><td><code>/api/books/1</code></td><td>Update a book</td></tr>
            <tr><td>DELETE</td><td><code>/api/books/1</code></td><td>Delete a book</td></tr>
            <tr><td>GET</td><td><code>/api/books/search?q=python</code></td><td>Search books</td></tr>
        </table>

        <h2>Try it!</h2>
        <p>Open your terminal and run:</p>
        <pre>curl http://127.0.0.1:5000/api/books</pre>
        <pre>curl http://127.0.0.1:5000/api/books/1</pre>
        <pre>curl -X POST -H "Content-Type: application/json" -d '{"title":"New Book","author":"You"}' http://127.0.0.1:5000/api/books</pre>
    </body>
    </html>
    """


@app.route("/api/books", methods=["GET"])
def get_books():
    """GET all books."""
    conn = get_db()
    books = conn.execute("SELECT * FROM books ORDER BY title").fetchall()
    conn.close()

    return jsonify({
        "count": len(books),
        "books": [dict(b) for b in books]
    })


@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """GET a single book by ID."""
    conn = get_db()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()

    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(dict(book))


@app.route("/api/books", methods=["POST"])
def create_book():
    """CREATE a new book."""
    data = request.get_json()

    if not data or not data.get("title") or not data.get("author"):
        return jsonify({"error": "Title and author are required"}), 400

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO books (title, author, year, genre, rating) VALUES (?, ?, ?, ?, ?)",
        (data["title"], data["author"], data.get("year"), data.get("genre"), data.get("rating", 0))
    )
    conn.commit()

    book = conn.execute("SELECT * FROM books WHERE id = ?", (cursor.lastrowid,)).fetchone()
    conn.close()

    return jsonify(dict(book)), 201  # 201 = Created


@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    """UPDATE an existing book."""
    conn = get_db()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()

    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    if not data:
        conn.close()
        return jsonify({"error": "No data provided"}), 400

    conn.execute(
        """UPDATE books SET
            title = ?, author = ?, year = ?, genre = ?, rating = ?
        WHERE id = ?""",
        (
            data.get("title", book["title"]),
            data.get("author", book["author"]),
            data.get("year", book["year"]),
            data.get("genre", book["genre"]),
            data.get("rating", book["rating"]),
            book_id
        )
    )
    conn.commit()

    updated = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()

    return jsonify(dict(updated))


@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    """DELETE a book."""
    conn = get_db()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()

    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Book '{book['title']}' deleted"})


@app.route("/api/books/search", methods=["GET"])
def search_books():
    """Search books by title or author."""
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Please provide a search query (?q=...)"}), 400

    conn = get_db()
    books = conn.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
        (f"%{query}%", f"%{query}%")
    ).fetchall()
    conn.close()

    return jsonify({
        "query": query,
        "count": len(books),
        "books": [dict(b) for b in books]
    })


# Initialize and run
init_db()

if __name__ == "__main__":
    print("\n  Books API running!")
    print("  Open http://127.0.0.1:5000\n")
    app.run(debug=True)

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add pagination. GET /api/books?page=1&per_page=10

# CHALLENGE 2: Add sorting. GET /api/books?sort=rating&order=desc

# CHALLENGE 3: Build a simple HTML frontend that uses YOUR API
# with JavaScript fetch() calls.

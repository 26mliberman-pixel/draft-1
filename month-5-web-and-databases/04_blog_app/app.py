"""
PROJECT 04: BLOG APPLICATION
===============================
A full CRUD web application with a database.

WHAT YOU'LL LEARN:
- Full CRUD operations in a web app
- More SQL (UPDATE, DELETE)
- HTML forms (GET vs POST)
- Flash messages
- Building a complete application
"""

from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your-secret-key-change-this"
DB_FILE = "blog.db"


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    return conn


def init_db():
    """Create the database tables."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT DEFAULT 'Anonymous',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# HTML template (in a real app, these would be separate files)
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Blog{% endblock %}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Georgia, serif; background: #f9f9f9; color: #333; }
        header { background: #2c3e50; color: white; padding: 20px; text-align: center; }
        header h1 { font-size: 2em; }
        header a { color: white; text-decoration: none; }
        nav { text-align: center; padding: 10px; background: #34495e; }
        nav a { color: #ecf0f1; text-decoration: none; margin: 0 15px; font-size: 1.1em; }
        nav a:hover { color: #3498db; }
        main { max-width: 800px; margin: 30px auto; padding: 0 20px; }
        .post { background: white; padding: 30px; margin: 20px 0; border-radius: 5px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .post h2 { margin-bottom: 10px; }
        .post h2 a { color: #2c3e50; text-decoration: none; }
        .post h2 a:hover { color: #3498db; }
        .post .meta { color: #888; font-size: 0.9em; margin-bottom: 15px; }
        .post .content { line-height: 1.8; }
        .actions { margin-top: 15px; }
        .actions a { margin-right: 10px; color: #3498db; text-decoration: none; }
        .btn { display: inline-block; padding: 8px 16px; background: #3498db; color: white;
               border: none; border-radius: 3px; text-decoration: none; cursor: pointer;
               font-size: 1em; }
        .btn:hover { background: #2980b9; }
        .btn-danger { background: #e74c3c; }
        .btn-danger:hover { background: #c0392b; }
        form { background: white; padding: 30px; border-radius: 5px;
               box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        label { display: block; margin: 15px 0 5px; font-weight: bold; }
        input[type="text"], textarea { width: 100%; padding: 10px; border: 1px solid #ddd;
            border-radius: 3px; font-size: 1em; font-family: inherit; }
        textarea { height: 300px; }
        footer { text-align: center; padding: 20px; color: #888; margin-top: 40px; }
    </style>
</head>
<body>
    <header><h1><a href="/">My Blog</a></h1></header>
    <nav>
        <a href="/">Home</a>
        <a href="/new">Write Post</a>
    </nav>
    <main>{% block content %}{% endblock %}</main>
    <footer>Built with Flask &amp; SQLite | Learning Python Month 5</footer>
</body>
</html>
"""

# Individual page templates
HOME_TEMPLATE = """
{% extends base %}
{% block title %}My Blog{% endblock %}
{% block content %}
    <h2 style="margin: 20px 0;">Recent Posts</h2>
    {% if posts %}
        {% for post in posts %}
        <div class="post">
            <h2><a href="/post/{{ post.id }}">{{ post.title }}</a></h2>
            <div class="meta">By {{ post.author }} | {{ post.created_at[:16] }}</div>
            <div class="content">{{ post.content[:200] }}{% if post.content|length > 200 %}...{% endif %}</div>
            <div class="actions">
                <a href="/post/{{ post.id }}">Read more</a>
            </div>
        </div>
        {% endfor %}
    {% else %}
        <div class="post">
            <p>No posts yet. <a href="/new">Write your first post!</a></p>
        </div>
    {% endif %}
{% endblock %}
"""

POST_TEMPLATE = """
{% extends base %}
{% block title %}{{ post.title }}{% endblock %}
{% block content %}
    <div class="post">
        <h2>{{ post.title }}</h2>
        <div class="meta">By {{ post.author }} | {{ post.created_at[:16] }}
            {% if post.updated_at != post.created_at %}
            | Updated: {{ post.updated_at[:16] }}
            {% endif %}
        </div>
        <div class="content">{{ post.content | replace('\\n', '<br>') | safe }}</div>
        <div class="actions" style="margin-top: 30px;">
            <a href="/edit/{{ post.id }}" class="btn">Edit</a>
            <a href="/delete/{{ post.id }}" class="btn btn-danger"
               onclick="return confirm('Delete this post?')">Delete</a>
            <a href="/" style="margin-left: 10px;">Back to all posts</a>
        </div>
    </div>
{% endblock %}
"""

FORM_TEMPLATE = """
{% extends base %}
{% block title %}{% if post %}Edit Post{% else %}New Post{% endif %}{% endblock %}
{% block content %}
    <h2 style="margin: 20px 0;">{% if post %}Edit Post{% else %}New Post{% endif %}</h2>
    <form method="POST">
        <label for="title">Title</label>
        <input type="text" name="title" id="title"
               value="{{ post.title if post else '' }}" required>

        <label for="author">Author</label>
        <input type="text" name="author" id="author"
               value="{{ post.author if post else '' }}" placeholder="Anonymous">

        <label for="content">Content</label>
        <textarea name="content" id="content" required>{{ post.content if post else '' }}</textarea>

        <br><br>
        <button type="submit" class="btn">{% if post %}Update{% else %}Publish{% endif %}</button>
        <a href="/" style="margin-left: 15px;">Cancel</a>
    </form>
{% endblock %}
"""


@app.route("/")
def home():
    conn = get_db()
    posts = conn.execute("SELECT * FROM posts ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template_string(HOME_TEMPLATE, base=BASE_TEMPLATE, posts=posts)


@app.route("/post/<int:post_id>")
def view_post(post_id):
    conn = get_db()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if not post:
        return "Post not found!", 404
    return render_template_string(POST_TEMPLATE, base=BASE_TEMPLATE, post=post)


@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form.get("author", "").strip() or "Anonymous"
        content = request.form["content"]

        conn = get_db()
        conn.execute(
            "INSERT INTO posts (title, author, content) VALUES (?, ?, ?)",
            (title, author, content)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template_string(FORM_TEMPLATE, base=BASE_TEMPLATE, post=None)


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    conn = get_db()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form.get("author", "").strip() or "Anonymous"
        content = request.form["content"]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn.execute(
            "UPDATE posts SET title=?, author=?, content=?, updated_at=? WHERE id=?",
            (title, author, content, now, post_id)
        )
        conn.commit()
        conn.close()
        return redirect(f"/post/{post_id}")

    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if not post:
        return "Post not found!", 404
    return render_template_string(FORM_TEMPLATE, base=BASE_TEMPLATE, post=post)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    conn = get_db()
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return redirect("/")


# Initialize and run
init_db()

if __name__ == "__main__":
    print("\n  Blog app running!")
    print("  Open http://127.0.0.1:5000\n")
    app.run(debug=True)

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add comments to posts. Create a comments table
# and let visitors leave comments on posts.

# CHALLENGE 2: Add categories/tags. Let authors tag their posts
# and let visitors filter by tag.

# CHALLENGE 3: Add a search feature — search posts by title or content.

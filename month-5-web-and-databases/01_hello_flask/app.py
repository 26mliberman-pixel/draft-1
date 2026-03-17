"""
PROJECT 01: HELLO FLASK
=========================
Your first web application!

WHAT YOU'LL LEARN:
- How web apps work (request → response)
- Flask basics — routes, templates, static files
- HTML basics
- Running a local web server

HOW TO RUN:
1. pip install flask
2. python app.py
3. Open http://127.0.0.1:5000 in your browser

WHAT IS FLASK?
Flask is a "web framework" — it handles all the complicated stuff
(like listening for requests, sending responses) so you can focus
on YOUR code. It's like a pre-built foundation for your house.
"""

from flask import Flask, render_template_string

# Create the Flask app
app = Flask(__name__)

# ============================================================
# LESSON: Routes
# ============================================================

# A ROUTE maps a URL to a Python function.
# When someone visits that URL, Flask runs the function
# and sends back whatever the function returns.

@app.route("/")
def home():
    """The home page — what people see at http://127.0.0.1:5000/"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My First Web App!</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1 { color: #333; }
            .card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                margin: 15px 0;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover { text-decoration: underline; }
            .nav { margin: 20px 0; }
            .nav a { margin-right: 15px; }
        </style>
    </head>
    <body>
        <h1>Welcome to My First Flask App!</h1>

        <div class="nav">
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/greet/World">Greet</a>
            <a href="/calculator">Calculator</a>
        </div>

        <div class="card">
            <h2>Hello, World!</h2>
            <p>This is a web page served by Python and Flask.</p>
            <p>Try visiting the other pages using the links above!</p>
        </div>

        <div class="card">
            <h2>How This Works</h2>
            <ol>
                <li>You type a URL in your browser</li>
                <li>Flask receives the request</li>
                <li>Flask finds the matching route function</li>
                <li>The function returns HTML</li>
                <li>Your browser displays the HTML</li>
            </ol>
        </div>
    </body>
    </html>
    """)


@app.route("/about")
def about():
    """The about page."""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>About</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            a { color: #007bff; text-decoration: none; }
        </style>
    </head>
    <body>
        <a href="/">&larr; Back to Home</a>
        <h1>About This App</h1>
        <p>This was built with Flask, a Python web framework.</p>
        <p>I'm learning Python and this is my Month 5 project!</p>
    </body>
    </html>
    """)


@app.route("/greet/<name>")
def greet(name):
    """Dynamic route — the URL contains a variable!
    Visit /greet/Alice or /greet/YourName
    """
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Greeting</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            .greeting { font-size: 2em; color: #333; }
            a { color: #007bff; text-decoration: none; }
        </style>
    </head>
    <body>
        <a href="/">&larr; Back to Home</a>
        <p class="greeting">Hello, {{ name }}!</p>
        <p>Try changing the name in the URL.</p>
        <p>Example: /greet/Alice, /greet/Python, /greet/YourName</p>
    </body>
    </html>
    """, name=name)


@app.route("/calculator")
def calculator():
    """A simple calculator page with a form."""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Calculator</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            form { background: white; padding: 20px; border-radius: 10px; }
            input, select { padding: 8px; margin: 5px; font-size: 16px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none;
                     border-radius: 5px; cursor: pointer; font-size: 16px; }
            .result { font-size: 1.5em; margin: 20px 0; }
            a { color: #007bff; text-decoration: none; }
        </style>
    </head>
    <body>
        <a href="/">&larr; Back to Home</a>
        <h1>Web Calculator</h1>
        <form action="/calculate" method="GET">
            <input type="number" name="a" placeholder="First number" step="any" required>
            <select name="op">
                <option value="add">+</option>
                <option value="sub">-</option>
                <option value="mul">x</option>
                <option value="div">÷</option>
            </select>
            <input type="number" name="b" placeholder="Second number" step="any" required>
            <button type="submit">Calculate</button>
        </form>
    </body>
    </html>
    """)


@app.route("/calculate")
def calculate():
    """Handle the calculator form submission."""
    from flask import request

    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 0))
    op = request.args.get("op", "add")

    if op == "add":
        result = a + b
        symbol = "+"
    elif op == "sub":
        result = a - b
        symbol = "-"
    elif op == "mul":
        result = a * b
        symbol = "x"
    elif op == "div":
        if b == 0:
            return "Can't divide by zero! <a href='/calculator'>Try again</a>"
        result = a / b
        symbol = "÷"
    else:
        result = 0
        symbol = "?"

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Result</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            .result { font-size: 2em; }
            a { color: #007bff; text-decoration: none; }
        </style>
    </head>
    <body>
        <p class="result">{{ a }} {{ symbol }} {{ b }} = {{ result }}</p>
        <a href="/calculator">Calculate again</a> | <a href="/">Home</a>
    </body>
    </html>
    """, a=a, b=b, symbol=symbol, result=round(result, 4))


# ============================================================
# Run the app!
# ============================================================

if __name__ == "__main__":
    print("\n  Starting Flask app...")
    print("  Open http://127.0.0.1:5000 in your browser!\n")
    app.run(debug=True)

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add a new route /time that shows the current date and time.

# CHALLENGE 2: Add a route /random that shows a random quote each time
# you refresh the page.

# CHALLENGE 3: Style the pages better with more CSS.
# Look up CSS tutorials if you want to learn more.

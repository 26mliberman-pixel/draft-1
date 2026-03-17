"""
PROJECT 02: PERSONAL PORTFOLIO WEBSITE
=========================================
Build your own portfolio to show off your projects!

WHAT YOU'LL LEARN:
- HTML structure (tags, elements)
- CSS styling (colors, layout, fonts)
- Flask templates with Jinja2
- Serving static files (images, CSS)
"""

from flask import Flask, render_template_string

app = Flask(__name__)

# Your projects data — update this with YOUR projects!
PROJECTS = [
    {
        "name": "Number Guessing Game",
        "description": "A CLI game where you guess a random number with hints.",
        "tech": "Python",
        "month": 2,
    },
    {
        "name": "Hangman",
        "description": "Classic word guessing game with ASCII art.",
        "tech": "Python",
        "month": 2,
    },
    {
        "name": "Expense Tracker",
        "description": "Track expenses with categories and save to JSON files.",
        "tech": "Python, JSON",
        "month": 3,
    },
    {
        "name": "Weather App",
        "description": "Get real weather data from the internet using APIs.",
        "tech": "Python, APIs",
        "month": 4,
    },
    {
        "name": "File Organizer",
        "description": "Automatically organize messy folders by file type.",
        "tech": "Python, OS module",
        "month": 4,
    },
]

SKILLS = [
    {"name": "Python", "level": 75},
    {"name": "HTML/CSS", "level": 40},
    {"name": "Git", "level": 30},
    {"name": "APIs", "level": 50},
    {"name": "SQL", "level": 20},
]

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} — Portfolio</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
        }

        /* Hero section */
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 20px;
            text-align: center;
        }
        .hero h1 { font-size: 3em; margin-bottom: 10px; }
        .hero p { font-size: 1.3em; opacity: 0.9; }

        /* Navigation */
        nav {
            background: #333;
            padding: 15px;
            text-align: center;
            position: sticky;
            top: 0;
        }
        nav a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
            font-size: 1.1em;
        }
        nav a:hover { color: #667eea; }

        /* Sections */
        section {
            max-width: 900px;
            margin: 0 auto;
            padding: 60px 20px;
        }
        section h2 {
            font-size: 2em;
            margin-bottom: 30px;
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }

        /* About */
        .about-text { font-size: 1.1em; line-height: 1.8; }

        /* Skills */
        .skill {
            margin: 15px 0;
        }
        .skill-name {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }
        .skill-bar {
            background: #e0e0e0;
            border-radius: 10px;
            height: 20px;
        }
        .skill-fill {
            background: linear-gradient(90deg, #667eea, #764ba2);
            height: 100%;
            border-radius: 10px;
            transition: width 0.5s;
        }

        /* Projects */
        .project-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }
        .project-card {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 25px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .project-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .project-card h3 { color: #667eea; margin-bottom: 10px; }
        .project-card .tech {
            display: inline-block;
            background: #f0f0f0;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            margin-top: 10px;
        }

        /* Contact */
        .contact-info { font-size: 1.1em; }
        .contact-info p { margin: 10px 0; }

        /* Footer */
        footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
        }
    </style>
</head>
<body>
    <nav>
        <a href="#about">About</a>
        <a href="#skills">Skills</a>
        <a href="#projects">Projects</a>
        <a href="#contact">Contact</a>
    </nav>

    <div class="hero">
        <h1>{{ name }}</h1>
        <p>Aspiring Python Developer</p>
    </div>

    <section id="about">
        <h2>About Me</h2>
        <p class="about-text">
            Hi! I'm a beginner programmer on a 6-month journey to learn Python.
            I started from zero and I've been building projects every month.
            This portfolio showcases what I've built so far. I'm passionate about
            learning and I get more capable every day!
        </p>
    </section>

    <section id="skills">
        <h2>Skills</h2>
        {% for skill in skills %}
        <div class="skill">
            <div class="skill-name">
                <span>{{ skill.name }}</span>
                <span>{{ skill.level }}%</span>
            </div>
            <div class="skill-bar">
                <div class="skill-fill" style="width: {{ skill.level }}%"></div>
            </div>
        </div>
        {% endfor %}
    </section>

    <section id="projects">
        <h2>Projects</h2>
        <div class="project-grid">
            {% for project in projects %}
            <div class="project-card">
                <h3>{{ project.name }}</h3>
                <p>{{ project.description }}</p>
                <span class="tech">{{ project.tech }}</span>
                <span class="tech">Month {{ project.month }}</span>
            </div>
            {% endfor %}
        </div>
    </section>

    <section id="contact">
        <h2>Contact</h2>
        <div class="contact-info">
            <p>Want to connect? Reach me at:</p>
            <p>Email: your.email@example.com</p>
            <p>GitHub: github.com/yourusername</p>
        </div>
    </section>

    <footer>
        <p>Built with Python &amp; Flask | 2026</p>
    </footer>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        TEMPLATE,
        name="Your Name Here",  # Change this!
        projects=PROJECTS,
        skills=SKILLS,
    )


if __name__ == "__main__":
    print("\n  Your portfolio is running!")
    print("  Open http://127.0.0.1:5000\n")
    app.run(debug=True)

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Personalize it! Add your real name, projects,
# and contact info. Add a photo of yourself.

# CHALLENGE 2: Add a "Blog" section where you write about
# what you learned each month.

# CHALLENGE 3: Make it mobile-responsive (it mostly is already,
# but test it and adjust the CSS if needed).

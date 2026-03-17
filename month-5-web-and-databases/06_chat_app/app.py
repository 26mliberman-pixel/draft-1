"""
PROJECT 06: SIMPLE CHAT APPLICATION
=======================================
A real-time-ish chat app! Your Month 5 capstone.

WHAT YOU'LL LEARN:
- Combining Flask, databases, and frontend
- JavaScript basics (for the browser)
- Auto-refreshing content
- Building a complete multi-user application

NOTE: This uses polling (checking for new messages every few seconds)
rather than true WebSockets, to keep it simple.
"""

from flask import Flask, render_template_string, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_FILE = "chat.db"


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat Room</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial; background: #1a1a2e; color: #eee; height: 100vh;
               display: flex; flex-direction: column; }

        header { background: #16213e; padding: 15px 20px; text-align: center; }
        header h1 { color: #e94560; }

        #login-screen {
            display: flex; align-items: center; justify-content: center;
            flex: 1; flex-direction: column;
        }
        #login-screen input {
            padding: 12px; font-size: 18px; border: none; border-radius: 5px;
            width: 300px; margin: 10px;
        }
        #login-screen button {
            padding: 12px 30px; font-size: 18px; background: #e94560;
            color: white; border: none; border-radius: 5px; cursor: pointer;
        }

        #chat-screen { display: none; flex: 1; flex-direction: column; }

        #messages {
            flex: 1; overflow-y: auto; padding: 20px;
        }
        .message {
            margin: 8px 0; padding: 10px 15px; border-radius: 10px;
            max-width: 70%; word-wrap: break-word;
        }
        .message.mine {
            background: #e94560; margin-left: auto;
        }
        .message.other {
            background: #16213e;
        }
        .message .user {
            font-size: 0.8em; color: #aaa; margin-bottom: 3px;
        }
        .message.mine .user { color: #ffccd5; }
        .message .time {
            font-size: 0.7em; color: #888; margin-top: 3px;
        }

        #input-area {
            display: flex; padding: 15px; background: #16213e;
        }
        #input-area input {
            flex: 1; padding: 12px; font-size: 16px; border: none;
            border-radius: 5px 0 0 5px; background: #0f3460; color: white;
        }
        #input-area button {
            padding: 12px 25px; background: #e94560; color: white;
            border: none; border-radius: 0 5px 5px 0; cursor: pointer;
            font-size: 16px;
        }

        #online { color: #aaa; font-size: 0.9em; }
    </style>
</head>
<body>
    <header>
        <h1>Chat Room</h1>
        <span id="online"></span>
    </header>

    <div id="login-screen">
        <h2>Enter your name to join</h2>
        <input type="text" id="username-input" placeholder="Your name..." maxlength="20">
        <button onclick="joinChat()">Join Chat</button>
    </div>

    <div id="chat-screen">
        <div id="messages"></div>
        <div id="input-area">
            <input type="text" id="message-input" placeholder="Type a message..."
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        let username = '';
        let lastMessageId = 0;

        function joinChat() {
            username = document.getElementById('username-input').value.trim();
            if (!username) return;

            document.getElementById('login-screen').style.display = 'none';
            document.getElementById('chat-screen').style.display = 'flex';
            document.getElementById('message-input').focus();

            // Start polling for new messages
            fetchMessages();
            setInterval(fetchMessages, 2000);  // Check every 2 seconds
        }

        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            if (!message) return;

            fetch('/api/messages', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, message: message })
            })
            .then(response => response.json())
            .then(data => {
                input.value = '';
                fetchMessages();  // Immediately fetch to show our message
            });
        }

        function fetchMessages() {
            fetch('/api/messages?after=' + lastMessageId)
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('messages');
                let shouldScroll = container.scrollHeight - container.scrollTop
                                   <= container.clientHeight + 50;

                data.messages.forEach(msg => {
                    const div = document.createElement('div');
                    div.className = 'message ' + (msg.username === username ? 'mine' : 'other');
                    div.innerHTML = '<div class="user">' + msg.username + '</div>'
                                  + '<div>' + escapeHtml(msg.message) + '</div>'
                                  + '<div class="time">' + msg.timestamp.slice(11, 16) + '</div>';
                    container.appendChild(div);
                    lastMessageId = msg.id;
                });

                if (shouldScroll && data.messages.length > 0) {
                    container.scrollTop = container.scrollHeight;
                }
            });
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(TEMPLATE)


@app.route("/api/messages", methods=["GET"])
def get_messages():
    after_id = request.args.get("after", 0, type=int)
    conn = get_db()
    messages = conn.execute(
        "SELECT * FROM messages WHERE id > ? ORDER BY id ASC",
        (after_id,)
    ).fetchall()
    conn.close()

    return jsonify({
        "messages": [dict(m) for m in messages]
    })


@app.route("/api/messages", methods=["POST"])
def post_message():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("message"):
        return jsonify({"error": "Username and message required"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO messages (username, message) VALUES (?, ?)",
        (data["username"][:20], data["message"][:500])  # Limit lengths
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"}), 201


# Initialize and run
init_db()

if __name__ == "__main__":
    print("\\n  Chat app running!")
    print("  Open http://127.0.0.1:5000 in multiple browser tabs!\\n")
    app.run(debug=True)

# ============================================================
# CHALLENGES & MONTH 5 CONCLUSION
# ============================================================

# CHALLENGE 1: Add "rooms" — users can join different chat rooms.

# CHALLENGE 2: Add typing indicators — show "Alice is typing..."

# CHALLENGE 3: Add message reactions (like/dislike).

# ============================================================
# CONGRATULATIONS! You've completed Month 5!
#
# You now know:
# - Flask web framework
# - HTML and CSS basics
# - SQLite databases and SQL
# - REST APIs
# - JavaScript basics
# - Full-stack web development!
#
# Final month: month-6-capstone/
# Put it ALL together!
# ============================================================
"""

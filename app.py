from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
from flask_session import Session
import sqlite3
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "lolmykeyisverysecure"  
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app, manage_session=False)

# ===== Users =====
users = {
    "admin": "adminpass",
    "elara": "shanlovesme",
    "huh_shanie": "ily",
}

# ===== Database =====
DB_NAME = "chat.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Run DB initialization on startup
init_db()

# ===== Routes =====
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error="Invalid credentials!")

    return render_template("login.html")


@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("login"))

    # Load previous messages from DB
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username, message, timestamp FROM messages ORDER BY id ASC")
    old_messages = c.fetchall()
    conn.close()

    return render_template("chat.html", username=session["username"], messages=old_messages)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

# ===== SocketIO Events =====
@socketio.on("message")
def handle_message(msg):
    if "username" in session:
        username = session["username"]

        # Save message to DB
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, msg))
        conn.commit()
        conn.close()

        # Broadcast to all users
        send({"username": username, "message": msg}, broadcast=True)




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))  # use 5002 locally instead of 5001
    debug_mode = (port == 5002)
    socketio.run(app, host="0.0.0.0", port=port, debug=debug_mode)





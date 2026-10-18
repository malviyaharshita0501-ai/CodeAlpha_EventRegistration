from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "event-registration-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "events.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            description TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            participant_name TEXT NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id),
            UNIQUE (event_id, email)
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    connection = get_db_connection()

    events = connection.execute("""
        SELECT events.*,
               COUNT(registrations.id) AS participant_count
        FROM events
        LEFT JOIN registrations ON events.id = registrations.event_id
        GROUP BY events.id
        ORDER BY events.date, events.time
    """).fetchall()

    connection.close()

    return render_template("index.html", events=events)


@app.route("/create-event", methods=["POST"])
def create_event():
    name = request.form.get("name", "").strip()
    date = request.form.get("date", "").strip()
    time = request.form.get("time", "").strip()
    description = request.form.get("description", "").strip()

    if not name or not date or not time:
        flash("Please enter the event name, date, and time.")
        return redirect(url_for("home"))

    connection = get_db_connection()

    connection.execute("""
        INSERT INTO events (name, date, time, description)
        VALUES (?, ?, ?, ?)
    """, (name, date, time, description))

    connection.commit()
    connection.close()

    flash("Event created successfully!")
    return redirect(url_for("home"))


@app.route("/register/<int:event_id>", methods=["POST"])
def register(event_id):
    participant_name = request.form.get("participant_name", "").strip()
    email = request.form.get("email", "").strip()

    if not participant_name or not email or "@" not in email:
        flash("Enter a valid name and email address.")
        return redirect(url_for("home"))

    connection = get_db_connection()

    event = connection.execute(
        "SELECT id FROM events WHERE id = ?", (event_id,)
    ).fetchone()

    if event is None:
        connection.close()
        flash("Event not found.")
        return redirect(url_for("home"))

    try:
        connection.execute("""
            INSERT INTO registrations (event_id, participant_name, email)
            VALUES (?, ?, ?)
        """, (event_id, participant_name, email))

        connection.commit()
        flash("Registration successful!")

    except sqlite3.IntegrityError:
        flash("This email is already registered for this event.")

    finally:
        connection.close()

    return redirect(url_for("home"))


@app.route("/registrations/<int:event_id>")
def view_registrations(event_id):
    connection = get_db_connection()

    event = connection.execute(
        "SELECT * FROM events WHERE id = ?", (event_id,)
    ).fetchone()

    participants = connection.execute("""
        SELECT participant_name, email
        FROM registrations
        WHERE event_id = ?
        ORDER BY participant_name
    """, (event_id,)).fetchall()

    connection.close()

    if event is None:
        flash("Event not found.")
        return redirect(url_for("home"))

    return render_template(
        "registrations.html",
        event=event,
        participants=participants
    )


@app.route("/cancel-registration/<int:event_id>", methods=["POST"])
def cancel_registration(event_id):
    email = request.form.get("email", "").strip()

    connection = get_db_connection()

    result = connection.execute("""
        DELETE FROM registrations
        WHERE event_id = ? AND email = ?
    """, (event_id, email))

    connection.commit()
    connection.close()

    if result.rowcount:
        flash("Registration cancelled successfully.")
    else:
        flash("No registration found for that email.")

    return redirect(url_for("home"))


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
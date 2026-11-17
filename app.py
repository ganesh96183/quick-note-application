from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "notes.db"


# Connect to database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create database table
def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Get all notes
@app.route("/api/notes", methods=["GET"])
def get_notes():
    conn = get_db()

    notes = conn.execute(
        "SELECT * FROM notes ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(note) for note in notes])


# Save a new note
@app.route("/api/notes", methods=["POST"])
def add_note():
    data = request.get_json()

    content = data.get("content", "").strip()

    if not content:
        return jsonify({"error": "Note cannot be empty"}), 400

    conn = get_db()

    cursor = conn.execute(
        "INSERT INTO notes (content, created_at) VALUES (?, ?)",
        (content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    note_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Note saved successfully",
        "id": note_id
    }), 201


# Update a note
@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json()
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"error": "Note cannot be empty"}), 400

    conn = get_db()

    cursor = conn.execute(
        "UPDATE notes SET content = ? WHERE id = ?",
        (content, note_id)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"message": "Note updated successfully"})


# Delete a note
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_db()

    cursor = conn.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"message": "Note deleted successfully"})


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
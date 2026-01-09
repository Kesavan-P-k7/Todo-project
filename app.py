from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table
def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

create_table()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

# Add task
@app.route("/add", methods=["POST"])
def add_task():
    data = request.json
    title = data.get("title")

    if not title:
        return jsonify({"error": "Task cannot be empty"}), 400

    conn = get_db_connection()
    conn.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", (title, 0))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task added successfully"})

# ✅ Update task checkbox status
@app.route("/update/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    completed = data.get("completed")

    conn = get_db_connection()
    conn.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?",
        (1 if completed else 0, task_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Task status updated"})

# Delete task
@app.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(debug=True)
# ✅ Update task checkbox status
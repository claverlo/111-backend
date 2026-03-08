from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


DB_NAME = "budget_manager.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)  # Opens a connection to the D.B. file named 'budget_manager.db'
    cursor = conn.cursor()  # Creates a cursor/tool that lets us send commands (SELECT, INSERT...) to the DB TIME:1:00 hour


# cursor.execute()
# Tells the database to run an SQL command.

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()  # Save changes to the D.B.
    conn.close()   # Close the connection to the D.B.


@app.get('/api/health')
def health_check():
    return jsonify({
        "status": "OK"
    }), 200

@app.post('/api/register')
def register():
    new_user = request.get_json()
    print(new_user)
    print(new_user["username"])
    print(new_user["password"])

    username = new_user["username"]
    password = new_user["password"]

    conn = sqlite3.connect(DB_NAME)  # Opens a connection to the D.B. file named 'budget_manager.db'
    cursor = conn.cursor()  # Creates a cursor/tool that lets us send commands (SELECT, INSERT...) to the DB
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "User registered successfully"
    }), 201

@app.get('/api/users')
def get_users():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Allow columns values to be retrieved by name, row["username"]
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()  # Retriev]s all rows from the result of the query
    print(rows)
    conn.close()


    users = []
    for row in rows:
        user = {
            "id": row["id"],
            "username": row["username"],
            "password": row["password"]
        }
        users.append(user)

    return jsonify({
        "success": True,
        "message": "Users retrieved successfully",
        "data": users
    }), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
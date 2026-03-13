#flask (small f) → the Flask library / package  Flask (big F) → the Flask class (tool) inside the library
# 1. “Python, go inside the flask library and bring me three tools so I can use them in this file.” 1. Flask 2.jsonfy 3. and request 
# 1. Flask   - used to create the web app
# 2. jsonify - used to send JSON responses
# 3. request - used to read incoming request data
from flask import Flask, jsonify, request

app = Flask(__name__) ## app = Flask(__name__) means you are creating the Flask web application and storing it in the variable named app.
# Flask → the class (tool) used to create a web server.
# __name__ → tells Flask which file is running this application.
# purpose → to create the Flask app so you can define routes like @app.get() and @app.post() that handle requests.

import sqlite3 # “Bring in the SQLite database library so Python can work with a database.”; It lets your program create, read, and write data in a database.
# pupose of this is import sqlite3 loads the SQLite library so your Python program can create, read, update, and save data in the budget_manager.db database file.


DB_NAME = "budget_manager.db" # Variable name  is the DB_NAME and Value stored  is the "budget_manager.db" and 
# DB_NAME = "budget_manager.db"-# the purpsoe of this is to  saves the name of the database file in a variable so the program can use it later.
# DB_NAME created by the programmer.(.db) tells people (and tools) that the file is a database file.) but the budget_manager is also chose by the programer.



def init_db():# What= means you are creating a function named init_db,
    #init_db() = purpose of it is to run these functions (connect() and cursor()).

    conn = sqlite3.connect(DB_NAME) # means Python opens the database file budget_manager.db and saves that connection in a variable
    #called conn so the program can talk to the database.
    # Without this line, Python cannot talk to the database.
    #You connect it to DB_NAME so Python knows which database file (budget_manager.db) to open and use. jol

    cursor = conn.cursor() # cursor= variable name;
    #conn is a variable that stores the connection created by sqlite3.connect(DB_NAME) so Python can access the SQLite database.
    #runs the SQL commands (like CREATE TABLE, INSERT, SELECT)


# cursor.execute()
# Tells the database to run an SQL command./ what ever is inside the cursor.execute
    #look at the note line starts at 134 for more notes
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
      )
    """)
#look at the note line starts at 155 for more notes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT NOT NULL,
            amount INT NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit() # Save changes to the D.B. automatically
    conn.close() # Close the connection to the D.B. automatically


# @app.route('/api/health', methods=["GET"])
# def health_check():
#   return jsonify({
#     "status": "OK"
#   }), HTTPStatus.OK

@app.get('/api/health')        # Creates an API endpoint at /api/health=http://localhost:5000/api/health is a URL, and the endpoint part is /api/health.
#http://localhost:5000/api/health is a URL where = http is the protocol, localhost is the name for the IP address 127.0.0.1,
#  5000 is the port, and /api/health is the endpoint.
# this comand is = “If someone sends a GET request to the URL /api/health, run the function below.”
#
def health_check():            # def health_check(): means you are creating a function named health_check that will run when the /api/health endpoint is requested.
    return jsonify({           # If someone goes to:http://127.0.0.1:5000/api/health it will show = "status": "OK"  
        "status": "Ok"         # Message saying the server is working
    }), 200                    # HTTP status codes= 200 = OK, 201 = Created, 204 = No Content, 404 = Not Found,
                                #500 = Server Error — these numbers tell the client what happened with


@app.post('/api/register')        # Creates an API endpoint at /api/register = http://localhost:5000/api/register is a URL, and the endpoint part is /api/register.
# http://localhost:5000/api/register is a URL where = http is the protocol, localhost is the name for the IP address 127.0.0.1,
# 5000 is the port, and /api/register is the endpoint.
# this command is = “If someone sends a POST request to the URL /api/register, run the function below.”

def register():# def register(): means you are creating a function named register that will run when the /api/register endpoint is requested.
    new_user = request.get_json() # new_user = request.get_json() means the server reads the JSON data sent in the request (from Thunder Client) 
# and stores that data in a variable called new_user so the program can use it.
    print(new_user) #print(new_user) just prints the data in the terminal so you can see what was received usign the thunder client
    print(new_user["username"])# print(new_user["username"]) means it prints the value of the "username" field from the JSON data stored in new_user to the terminal.
# To test this: send a POST request in Thunder Client to http://127.0.0.1:5000/api/register,
# click Body → JSON, add {"username":"leo","password":"1234"}, then press Send so the
# program prints the username and password in the terminal.
    print(new_user["password"])


# this two needs to be inside the @app.post
    username = new_user["username"]# username = new_user["username"] → gets the "username" value from the JSON data stored in new_user and saves it in the variable username
    password = new_user["password"]# password = new_user["password"] → gets the "password" value from the JSON data stored in new_user and saves it in the variable password

    conn = sqlite3.connect(DB_NAME) # means Python opens the database file budget_manager.db and saves that connection in a variable
    #called conn so the program can talk to the database.
    # Without this line, Python cannot talk to the database.
    #You connect it to DB_NAME so Python knows which database file (budget_manager.db) to open and use. jol

    cursor = conn.cursor() # cursor= variable name;
    #conn is a variable that stores the connection created by sqlite3.connect(DB_NAME) so Python can access the SQLite database.
    #runs the SQL commands (like CREATE TABLE, INSERT, SELECT)


    #cursor.excute means to excecute everyting inside this parenthesis() look at line # 171 for the whats the meaning of those inside the ()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password)) # Execute SQL statement
# cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
# means the program runs an SQL command to add a new row into the users table,
# using the values stored in the variables username and password
# example: if username = "leo" and password = "1234", the database will store ("leo", "1234") as a new user.

    conn.commit() # Save changes to the Database automatically
    conn.close() # Close the connection to the D.B. automatically

    return jsonify({
    "success": True, # if success == true → show success message
    "message": "User registered successfully"
    }), 201


@app.get('/api/users')  # Creates an endpoint /api/users that runs when someone sends a GET request to get the list of users.
def get_users():       # means you are creating a function named get_users, = purpose of it is to run these functions anthuinig bellow in ()


    conn = sqlite3.connect(DB_NAME) # # Connects to the SQLite database file.name DB_NAME
    conn.row_factory = sqlite3.Row # Allows columns values to be retrieved by name, row["username"]/makes database rows behave like a dictionary instead of a tuple.
    # withiut factory= row = (1, "john", "1234") liek a tuple but with it  row = {"id":1, "username":"john", "password":"1234"}
    # pupsoe it is to access by name instead of number= from this row[1] to this ow["username"]
    cursor = conn.cursor() # cursor= variable name;
    #conn is a variable that stores the connection created by sqlite3.connect(DB_NAME) so Python can access the SQLite database.


    #cursor.execute()runs the SQL commands (like CREATE TABLE, INSERT, SELECT)tells it to run it.
    cursor.execute("SELECT * FROM users") # SELECT means= Tells the database you want to read/get data;* Means give me all columns in the table.
    rows = cursor.fetchall() # Retrieves all rows from the result of the query.
    print(rows)#This line prints the data that came from the database to the terminal or console.
    conn.close() # Close the connection to the D.B. automatically
    # # Rule: you dont put comitt here cause yuour jsut reading data
# GET = only reads data → no conn.commit()
# POST = adds data → need conn.commit()
# PUT/UPDATE = changes data → need conn.commit()
# DELETE = removes data → need conn.commit()
# commit() saves database changes permanently

    users = [] #Creates an empty list called users./You create users = [] so you can collect all the users from the database into one list.
    for row in rows:  #Go through each row in the rows list one by one./ for row in rows:  # Loop through each database row one by one
        user = {  # Creates a dictionary called user.
            "id": row["id"], #Take the id from the database row and store it as "id".
            "username": row["username"], # Take the username from the database row and store it as "username".
            "password": row["password"] #Take the password from the database row and store it as "password".
        }
        users.append(user)  #It adds one item to the end of a list. to test it do the folowing
      # To test in Thunder Client:
# 1. Create a request
# 2. Method: GET
# 3. URL: http://127.0.0.1:5000/api/users
# 4. Click Send
# 5. Look at the response → you should see the user inside the list


    return jsonify({
        "success": True,
        "message": "Users retrieved successfully",
        "data": users
    }), 200


# A path parameter lets you choose a specific item/id etc... in the URL.
# http://127.0.0.1:5000/api/users/3
@app.get('/api/users/<int:user_id>') #Creates an endpoint /api/users that runs when someone sends a GET request to get the list of users.
# uses this user_id = 3  to this /api/users/3 . Basically acessing itthe user id that you want to view.
def get_user_by_id(user_id): # means you are creating a function named get_user_by_id, = purpose of it is to run the functions anything below in ()
    conn = sqlite3.connect(DB_NAME) # # Connects to the SQLite database file.name DB_NAME
    conn.row_factory = sqlite3.Row # Allows columns values to be retrieved by name, row["username"]/makes database rows behave like a dictionary instead of a tuple.
    # withiut factory= row = (1, "john", "1234") liek a tuple but with it  row = {"id":1, "username":"john", "password":"1234"}
    # pupsoe it is to access by name instead of number= from this row[1] to this ow["username"]
    cursor = conn.cursor() # cursor= variable name;
    #conn is a variable that stores the connection created by sqlite3.connect(DB_NAME) so Python can access the SQLite database.
    #runs the SQL commands (like CREATE TABLE, INSERT, SELECT)
    cursor.execute("SELECT id, username FROM users WHERE id=?", (user_id,))#cursor.execute()runs the SQL commands (like CREATE TABLE, INSERT, SELECT)tells it to run it.
    # SELECT id, username → get the id and username 
    #FROM users → from the users table
    #WHERE id= The database is waiting for a number.
    # ? = a place holder
    #The purpose of user_id is to tell the database which user you want. it also comes from here def get_user_by_id(user_id):

    row = cursor.fetchone()  #Give me the first result from the database query.


    if not row:
        conn.close()#If no data (no row) was returned from the database, close the connection.

        return jsonify({
            "success": False,
            "message": "User not found"    
        }), 404
    else:
        user_information = {
            "id": row["id"], 
            "username": row["username"] 
        }
        
        conn.close()

        return jsonify({
            "success": True,
            "message": "User retrieved successfully",
            "data": user_information
        }), 200


# update user
@app.put('/api/users/<int:user_id>')
def update_user(user_id):
    updated_user = request.get_json()
    username = updated_user["username"]
    password = updated_user["password"]
    print(updated_user)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * from users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close() 
        return jsonify({
            "success": False,  
            "message": "User not found"
        }), 404

    cursor.execute("UPDATE users SET username=?, password=? WHERE id=?", (username, password, user_id))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "User updated successfully",
    }), 200


# delete user
@app.delete('/api/users/<int:user_id>')
def delete_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id=?",(user_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404 

    cursor.execute("DELETE FROM users WHERE id=?",(user_id,))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "User deleted successfully"
    }), 200


# ------------ Expenses ------------
@app.post('/api/expenses')
def create_expense():
    new_expense = request.get_json()
    print(new_expense)

    title = new_expense["title"]
    description = new_expense["description"]
    amount = new_expense["amount"]
    date = new_expense["date"]
    category = new_expense["category"]
    user_id = new_expense["user_id"]

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # make rows behave like dicts
    cursor = conn.cursor()

    cursor.execute(""" 
                INSERT INTO expenses (title, description, amount, date, category, user_id) 
                VALUES (?, ?, ?, ?, ?, ?)""", 
                (title, description, amount, date, category, user_id))
    conn.commit()
    conn.close()

    return jsonify({
        "success": False,
        "message": "Expense created successfully"
    }), 201


if __name__ == "__main__":
    init_db()
    app.run(debug=True)



    
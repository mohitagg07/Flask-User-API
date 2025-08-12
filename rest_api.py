from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "users.json"

# Load existing users from file
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save users to file
def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

users_db = load_users()

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the User Management REST API",
        "routes": {
            "GET /users": "Fetch all users",
            "GET /users/<username>": "Fetch a specific user",
            "POST /users": "Create a new user",
            "PUT /users/<username>": "Update an existing user",
            "DELETE /users/<username>": "Delete a user"
        }
    })

# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"total_users": len(users_db), "users": users_db})

# Get a specific user
@app.route("/users/<username>", methods=["GET"])
def get_user(username):
    user = users_db.get(username)
    if user:
        return jsonify({username: user})
    return jsonify({"error": "User not found"}), 404

# Create a new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password or not email:
        return jsonify({"error": "Username, password, and email are required"}), 400
    if username in users_db:
        return jsonify({"error": "User already exists"}), 409

    users_db[username] = {"password": password, "email": email}
    save_users(users_db)
    return jsonify({"message": f"User '{username}' created successfully"}), 201

# Update a user
@app.route("/users/<username>", methods=["PUT"])
def update_user(username):
    if username not in users_db:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    users_db[username].update(data)
    save_users(users_db)
    return jsonify({"message": f"User '{username}' updated successfully"})

# Delete a user
@app.route("/users/<username>", methods=["DELETE"])
def delete_user(username):
    if username in users_db:
        del users_db[username]
        save_users(users_db)
        return jsonify({"message": f"User '{username}' deleted successfully"})
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)


import requests

# Create a new user
response = requests.post("http://127.0.0.1:5000/users", json={
    "username": "mohit",
    "password": "1234",
    "email": "mohit@example.com"
})
print(response.json())

# Get all users
print(requests.get("http://127.0.0.1:5000/users").json())

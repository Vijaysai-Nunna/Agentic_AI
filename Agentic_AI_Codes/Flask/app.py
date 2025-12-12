from flask import Flask, request, jsonify

import json
import os
import logging

app = Flask(__name__)

DATA_FILE = "users.json"

@app.route("/Welcome")
def hello():
    return"elcome to User Management Service.You ae at Landing page of API."

@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    users = load_users()
    users.append(data)
    save_users(users)
    return jsonify({"Message" : "User Added Succesfully", "Code" : "200"})
    


#Storage -JSON storage

def load_users():
    if not os.path.exists(DATA_FILE):
        return[]
    with open("user.json","r") as f:
        return json.load(f)
    
def save_users():
    with open(DATA_FILE,"w") as f:
        return json.load(f)

if __name__ == "__main__":
    app.run(debug=True,port=5000)
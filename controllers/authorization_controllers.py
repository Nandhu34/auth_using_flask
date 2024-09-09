# controllers/authorization_controllers.py
from flask import jsonify
from helpers.db_creation import new_user_collection

def register_new_user(data):
    # Process data here
    print(data )


    return jsonify({"data": f"Register new user with data {data}"})

def login_user(data):
    # Process data here
    return jsonify({"data": f"Login with data {data}"})

def forget_password(data):
    # Process data here
    return jsonify({"data": f"Forget password with data {data}"})

def reset_password(data):
    # Process data here
    return jsonify({"data": f"Reset password with data {data}"})

def logout(data):
    # Process data here
    return jsonify({"data": f"Logout with data {data}"})

def edit_user_details(data):
    # Process data here
    return jsonify({"data": f"Edit user details with data {data}"})

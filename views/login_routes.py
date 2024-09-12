# views/login_routes.py
from flask import Blueprint, request, jsonify
from controllers.authorization_controllers import register_new_user, login_user, forget_password, reset_password, logout, edit_user_details
from validation.validate_register_new_user import RegisterDetailsValidating,ValidationError,login_validation,forget_password_validation
from models.check_user_presence import check_user_presnce
authorization = Blueprint('auth', __name__)

@authorization.route('/register', methods=['POST'])
def regis_user():
    data = request.json  # or request.form for form data
    try:
        user_data = RegisterDetailsValidating(**data)
        user_data = user_data.dict()
        print(user_data,"user data")
        data = register_new_user(user_data)
        print(data)
        if data['status']== "error":
            return jsonify({"errors": data['error']}), 400
        else :
            response_from_db = check_user_presnce(data['data'])
            if response_from_db['status']=="error":
                return ({"data":f"user aldrdy registered try loghin  "}),200
            else:
                 return ({"data":response_from_db['data']}),400

       
    except ValidationError as e:
         return jsonify({"errors": e.errors()}), 400


@authorization.route('/login', methods=['POST'])
def log_in():
    data = request.json  # or request.form for form data
    data = login_validation(**data)
    data = data.dict()
    print(" data after validation ",data)
    response_from_login = login_user(data)
    
    try :
        print(response_from_login.keys())
        print(" try block ")
        
        if 'status' in response_from_login.keys() :
            return ({"data":"no accout foun d just sign in "})
    except Exception as e :

        print(e)
        print(" except block in login ")
        if response_from_login:
            

            return ({"data":"loging in "})
        else :
            return ({"data":"password does not match "})
    return ({"data":"ncdn"})
    


@authorization.route('/forget_password', methods=['POST'])
def for_password():
    data = request.json
    try :
        forget_password_validation(**data)
    except  Exception :
        return ({"success":"error","data":"validation error in the inputted data"}),300
    forget_password(data)
    return forget_password(data)

@authorization.route('/reset_password', methods=['POST'])
def reset_pass():
    data = request.json
    return reset_password(data)

@authorization.route('/logout', methods=['POST'])
def logs_out():
    data = request.json
    return logout(data)

@authorization.route('/edit_user_details', methods=['POST'])
def edit_details():
    data = request.json
    return edit_user_details(data)

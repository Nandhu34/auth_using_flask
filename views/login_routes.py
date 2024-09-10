# views/login_routes.py
from flask import Blueprint, request, jsonify
from controllers.authorization_controllers import register_new_user, login_user, forget_password, reset_password, logout, edit_user_details
from validation.validate_register_new_user import RegisterDetailsValidating,ValidationError
from models.check_user_presence import check_user_presnce
authorization = Blueprint('auth', __name__)

@authorization.route('/register', methods=['POST'])
def regis_user():
    data = request.json  # or request.form for form data
    try:
        user_data = RegisterDetailsValidating(**data)
        user_data = user_data.dict()

        print(user_data,"user dat a")
        data = register_new_user(user_data)
        print(data )
        if data['status']== "error":
            return jsonify({"errors": data['error']}), 400
        else :
            response_from_db = check_user_presnce(data['data'])
            if response_from_db['status']=="error":
                return ({"data":f"user aldrdy registered try loghin  "}),200
            else:
                 return ({"data":response_from_db['data']}),400

        # data = data.get_data(as_text=True)
        
       
    

    except ValidationError as e:
         return jsonify({"errors": e.errors()}), 400


@authorization.route('/login', methods=['POST'])
def log_in():
    data = request.json  # or request.form for form data
    return login_user(data)

@authorization.route('/forget_password', methods=['POST'])
def for_password():
    data = request.json
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

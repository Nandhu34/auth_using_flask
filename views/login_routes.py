# views/login_routes.py
from flask import Blueprint, request, jsonify , redirect ,url_for
from controllers.authorization_controllers import register_new_user, login_user, forget_password, reset_password, logout, edit_user_details
from validation.validate_register_new_user import RegisterDetailsValidating,ValidationError,login_validation,forget_password_validation,UserProfileUpdate
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
                from app import home_route

                return home_route()
                # return ({"data":response_from_db['data']}),200
            

       
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
            

            # return ({"data":"loging in "})
            from app import home_route
            return home_route()

            # return redirect (url_for('home_route'))
        else :
            return ({"data":"password does not match "})

    return ({"data":"logged in successfully"})
    


@authorization.route('/forget_password', methods=['POST'])
def for_password():
    data = request.json
    try :
        forget_password_validation(**data)
    except  Exception  as e:
        return ({"success":"error","data":f"validation error in the inputted data{str(e)}"}),300
    
    print("validation over ")
    # forget_password(data)

    return forget_password(data)

@authorization.route('/reset_password/token=<token>', methods=['POST'])
def reset_pass(token):
    body_data = request.json
    print(body_data)

    
    current_url = request.base_url
    splitted_data = current_url.split('=')
    token = splitted_data[1]

    print(token )

    return reset_password(token,body_data['new_password'])

@authorization.route('/logout', methods=['POST'])
def logs_out():
    data = request.json
    return logout(data)




@authorization.route('/update_profile',methods = ['PUT'])
def edit_details():
    data = request.json
    try :
         data_after_validation = UserProfileUpdate(**data )
    except Exception as e:
        return({" status":"error","message":str(e)})
    return edit_user_details(data)


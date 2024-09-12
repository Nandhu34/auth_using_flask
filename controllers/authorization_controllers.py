# controllers/authorization_controllers.py
from flask import jsonify
from models.db_creation import new_user_collection
from  helpers.update_data_in_cookie import update_data_into_cookie
from helpers.auth_helpers import get_access_token,get_refresh_token,hash_password,decrypt_password

from models.check_user_presence import check_user_presnce,check_login,update_tokens_while_login
def register_new_user(data):
    # Process data here
    print(data )
    username = data['username']
    email=data['email']
    mobile_number = data['mobile_number']
    role= data['role']
    raw_data = {"username":username,"email":email,"mobile_number":mobile_number,'role':role}
    token = get_access_token(raw_data)
    print(" toekn generated ",token)
    if token: 
        data['access_token'] = token
    else:
        print(" access token errrror ")
        data['access_token']=""
        return ({"error":"access token not generated","status":"error"})
    
    refresh_toekn = get_refresh_token(raw_data)
    if refresh_toekn:
        data['refresh_token'] = refresh_toekn
    else :
        print(" refresh token error ")
        data['refresh_token'] =""
        return ({"error":"Refresh  token not generated","status":"error"})
    cookie_data ={"refresh_toekn":refresh_toekn,"access_token":token}
    # update_data_in_cookie(cookie_data)
    hashed_password = hash_password(data['password'])
    if hashed_password:
        data['password'] = hashed_password
    else:
        return ({"error":"hashing password is not generated","status":"error"})


    return ({"status":"success","data": data})


def login_user(data):
    # Process data here
    print(data)
    original_password = data['password']
    res_from_db = check_login(data)
    print(res_from_db)
    if res_from_db['status']=='success':
        print(" no dat afpounds ")
        return ({"status":"error","data":"no account found "})
    else: 

        data = res_from_db['data']
        print(original_password,res_from_db['data']['password'])
        if decrypt_password(original_password,res_from_db['data']['password']):
            print(" true - password matched ")
            username = data['username']
            email=data['email']
            mobile_number = data['mobile_number']
            role= data['role']
            raw_data = {"username":username,"email":email,"mobile_number":mobile_number,'role':role}
            token = get_access_token(raw_data)
            
            refresh_toekn = get_refresh_token(raw_data)
            cookie_data ={"refresh_toekn":refresh_toekn,"access_token":token}
            update_data_into_cookie(cookie_data)
            update_tokens_while_login(token,refresh_toekn,email)
            

                    

            return True 
        else:
            print(" password does not matched")
            return False 
        



    
    return jsonify({"data": f"Login with data {data}"})

def forget_password(data):
    from helpers.send_mail_to_email import send_mail
    return send_mail()
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

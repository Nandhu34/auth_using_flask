# controllers/authorization_controllers.py
from flask import jsonify,session
from models.db_creation import new_user_collection
from  helpers.update_data_in_cookie import update_data_into_cookie
from helpers.auth_helpers import get_access_token,get_refresh_token,hash_password,decrypt_password,check_expired,get_token_data
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

    cookie_data ={"refresh_token":refresh_toekn,"access_token":token}
    update_data_into_cookie(cookie_data)
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
            cookie_data ={"refresh_token":refresh_toekn,"access_token":token}
            update_data_into_cookie(cookie_data)
            update_tokens_while_login(token,refresh_toekn,email)
            

                    

            return True 
        else:
            print(" password does not matched")
            return False 
        



    
    return jsonify({"data": f"Login with data {data}"})

def forget_password(data):
    data = new_user_collection.find_one({"email":data['email']})
    if data !=None :
        from helpers.send_mail_to_email import send_mail
        return send_mail(data)
    else :


         return jsonify({"data": f"user id not found  {data}"})

def reset_password(data,new_password):
    hashed_password = hash_password(new_password)
    print(" printing hashing password ")
    print("token ",data)
    
    
    # check_token = new_user_collection.find_one({"reset_password_token":data,"email":hashed_password['email']})
    # if check_token==None :
    #     return ({"status":"error","data":"this is not the token that is generated for this email"})
    # check_token_used = new_user_collection.find_one({"reset_password_token":data,"reset_password_token_expire":True,"email":hash_password['email']})
    # if check_token_used :
    #     return ({"status":"error","data":"token has been used aldredy "})
    # print(" reset password ")

    print(data)
    result_from_token_expired = check_expired(data)
    print(result_from_token_expired)
    if result_from_token_expired:
        print(" token expired")
        return ({"status":"success","data":"link expired please request link again"})
    else:
        token_decode = get_token_data(data)
        print(" token data",token_decode)
        check_token = new_user_collection.find_one({"reset_password_token":data,"email":token_decode['email']})
        if check_token==None :
            return ({"status":"error","data":"this is not the token that is generated for this email"})
        check_token_used = new_user_collection.find_one({"reset_password_token":data,"reset_password_token_expire":True,"email":token_decode['email']})
        if check_token_used :
            return ({"status":"error","data":"token has been used aldredy "})
            

        data_from_db = new_user_collection.find_one({"email":token_decode['email']})
        print(data_from_db)
        payload_token  = {"username":data_from_db['username'],"email":data_from_db['email'],"mobile_number":data_from_db['mobile_number'],'role':data_from_db['role']}
        new_refresh_token = get_refresh_token(payload_token)
        new_access_token = get_access_token(payload_token)
        update_status = new_user_collection.update_one({"email":token_decode['email']},{"$set":{"reset_password_token_expire":True,"access_token":new_access_token,"refresh_token":new_refresh_token,"password":hashed_password}})
        
        print(update_status.modified_count)
        if update_status.modified_count==1:
           cookie_data ={"refresh_token":new_refresh_token,"access_token":new_access_token}
           update_data_into_cookie(cookie_data)
           return ({"data":f"new password has been reseted  {update_status.upserted_id}","status":"success"})
    # Process data here
        else :
            return ({"data":f"password not updated please try again later","status":"error"})
    
    # return jsonify({"data": f"Reset password with data {data}"})

def logout(data):
    session['logged_in']=False 
    session['data']=None
    print(dict(session))
    # Process data here

    return jsonify({"data": f"Logout with data {data}"})

def edit_user_details(data):
    # Process data here
    user_enetered_password = data['password']
    print(session['data'])
    access_token = session['data']['access_token']
    
    user_data = new_user_collection.find_one({"access_token":access_token})
    print(user_data)
    db_password  = user_data['password']
    result_from_password_comparison= decrypt_password(user_enetered_password,db_password)
    print(result_from_password_comparison, "res from password ")
    if  result_from_password_comparison :

        
        # print(data )
        data.pop('password',None )

        print(data )
        find_qwery = {"access_token":access_token}
        update_qwery = {"$set":data}
        print(find_qwery,update_qwery)
        update_user_data = new_user_collection.update_one(find_qwery,update_qwery)  
        if update_user_data.modified_count ==1 :
              return jsonify({"data": f"Edit user details with data {data}"})
        else:
            return ({"status":"not_updated","message":"no new data has been updated.. all you priovided data is old data  "})
         
    else:
        print(" password npot matched ")
        return ({"status":"error","message":"password not matched "}) 
    
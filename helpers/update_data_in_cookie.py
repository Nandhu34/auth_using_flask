from flask import Flask , make_response ,jsonify,request,session
import json
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)




def update_data_into_cookie(data):
    print(" cookie e e e e ")
    print(data)
    # data = {"sample_key": "sample_value"}  

    data_str = json.dumps(data)
    print(data_str)
    session['data'] = data
    print(" session data ")
    print(session['data'])

    # resp =make_response(jsonify({"login":True}))
    # get_jwt_identity(resp,data_str)
    # set_access_cookies(resp,data_str)
    # print(request.cookies.get())
    # print(get_jwt_identity())
    # resp = make_response()
    # resp.set_cookie('token', data_str, httponly=True, samesite='Strict', secure=True)
    # print(" data update dinto  cookie ")
    # token_cookie = request.cookies.get('token')
    # print(token_cookie)
    # return resp 

# update_data_into_cookie({"data":"sample_data"})


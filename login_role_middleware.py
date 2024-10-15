from functools import wraps 
from helpers import auth_helpers
from flask import request 

def check_token_and_role(required_role):
    def declare_function(funct):
        @wraps(funct)
        def  function_defanition (*args, **kwargs):
            token = str(request.headers.get('Authorization'))
            
            if not token :
                return ({"success":False ,"warning":"no tokem found in request"})
            else:
                # print(token )
                # print(type(str(token)))
                splitted = token.split(' ')[1]
                result_from_token = auth_helpers.get_token_data(splitted )
                # print(result_from_token)
                if  result_from_token == True  :
                    return ({"success":False,"warning":"something wrong in token! try after sometime"})

                else:
                    print(result_from_token)
                    if result_from_token['role'] in required_role:
                        return funct(*args,**kwargs)
                    else:
                        return ({"status":False, "warning":"Role mismatch! authorization error"})


           
            return funct(*args , **kwargs)
        return function_defanition
    return declare_function


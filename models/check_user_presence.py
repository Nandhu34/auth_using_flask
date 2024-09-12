from .db_creation import new_user_collection
from  datetime import datetime


def check_user_presnce(data ):

    print(data)
    check = new_user_collection.find_one({"email":data['email']})
    if check == None :
        ins= new_user_collection.insert_one(data)

        print(ins.inserted_id)
        return ({"status":"success","data":f"data inserted into db {ins.inserted_id}"})
    else :
        print(" data not present ")
        return ({"status":"error","data":check})
    



def check_login(data ):

    print(data)
    check = new_user_collection.find_one({"email":data['email']})
    if check == None :
        # ins= new_user_collection.insert_one(data)
        # print(ins.inserted_id)
        return ({"status":"success","data":"no data found  "})
    else :
        print(" data  present ")
        return ({"status":"error","data":check})
    


def update_tokens_while_login(access_token,refresh_toeken, email):
    new_user_collection.update_one({"email":email},{"$set":{"access_token":access_token,"refresh_token":refresh_toeken,"date_of_last_login":datetime.now().isocalendar()}}) 
    print(" toekn has been updated ")

    return True 


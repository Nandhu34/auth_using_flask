from .db_creation import new_user_collection
def check_user_presnce(data ):

    print(data)
    check = new_user_collection.find_one({"email":data['email']})
    if check == None :
        ins= new_user_collection.insert_one(data)
        print(ins.inserted_id)
        return ({"status":"success","data":f"data inserted into db {ins.inserted_id}"})
    else :
        return ({"status":"error","data":f"user aldredy present in db"})
    


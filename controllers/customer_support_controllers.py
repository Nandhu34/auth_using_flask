
from flask import session , request 
from models import db_creation
import  uuid 
from datetime import datetime
# from faker import Faker

# fake = Faker()

def add_new_support(category,message):
    
    status = "support_submitted"
    print(session['email'])
    check_user_existance = db_creation.customer_support_collection.find_one({"email":session['email']})
    # print(check_user_existance)
    if  check_user_existance == None :
        new_data = {"email":session['email'], "support_request":[{"support_id":str(uuid.uuid4()), "category":category,"date_of_generation":datetime.now(),"message":message, "status":status}]}
        ins = db_creation.customer_support_collection.insert_one(new_data)
        if ins.inserted_id:
            return ({"status":True ,"message":"support request has been send to the admin"})
        else:
            return ({"status":False ,"warning":"support request is not sent try later"})
    else:
        updation_data = db_creation.customer_support_collection.update_one({"email":session['email']},{"$push":{"support_request":{"support_id":str(uuid.uuid4()), "category":category,"date_of_generation":datetime.now(),"message":message, "status":status}}})
        if updation_data.matched_count ==1 :
            return ({"status":True ,"message":"data has been updated in old document"})
        else:
            return ({"status":False ,"warning":"support request is not sent try later"})


def  view_all_customer_support():
        
    check_user_existance = db_creation.customer_support_collection.find_one({"email":session['email']})
    if check_user_existance==None :
        return ({"status":False,"message":"this user has not send any support request"})
    else :
        return ({"success":True ,"data":check_user_existance['support_request']})

def view_specific_customer_support(support_id):
    agg_qwery=[
    {
        '$match': {
            'email': session['email']
        }
    }, {
        '$project': {
            'support_request': {
                '$filter': {
                    'input': '$support_request', 
                    'as': 'inn', 
                    'cond': {
                        '$eq': [
                            '$$inn.support_id', support_id
                        ]
                    }
                }
            },
             '_id': 0
        }
    }
]
    check_data = list(db_creation.customer_support_collection.aggregate(agg_qwery))
    if len(check_data)==0:
        return ({"success":False,"message":"no data found"})
    else:
        return ({"success":True,"data":check_data})
    



# # update_response_status and message 

def update_message_from_admin(support_id,admin_status,message_from_admin):
        
    search_qwery={"email":session['email'],"support_request.support_id":support_id}
    update_qwery = {"$set":{"support_request.$.status":admin_status,"support_request.$.admin_message":message_from_admin}}
    print(search_qwery,update_qwery)
    upd_cus_support = db_creation.customer_support_collection.update_one(search_qwery ,update_qwery)
    # print(email)
    if upd_cus_support.modified_count ==1:
        return ({"success":True,"message":f"status has been updated for support id {support_id}"})
    else :
        return ({"success":False,"message":"status not updated"})



def  update_the_message_from_user(new_message,support_id):
        
    search_qwery={"email":session['email'],"support_request.support_id":support_id}
    update_qwery = {"$set":{"support_request.$.message":new_message}}

    upd_cus_support = db_creation.customer_support_collection.update_one(search_qwery ,update_qwery)
    if upd_cus_support.modified_count ==1:
        return ({"message":f"status has been updated for support id {support_id}"})
    else :
        return ({"success":False,"message":"status not updated"})



def delete_specific_support(support_id): 
    search_qwery = {"email":session['email']}

    del_doc = db_creation.customer_support_collection.update_one({"email":session['email'],"support_request.support_id":support_id},{"$pull":{"support_request":{"support_id":support_id}}})
    if del_doc.modified_count==1:
        return({"message":f"support id {support_id} has been deleted"})
    else:
         return({"success":False,"message":"please try again later"})


def delete_complete_support():
        

    del_doc = db_creation.customer_support_collection.delete_one({"email":session['email']})
    if del_doc.deleted_count ==1:
        return ({"success":True,"message":"all reviews deleted"})
    else:
         return({"success":False,"message":"please try again later"})
    
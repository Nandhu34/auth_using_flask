from models import db_creation
from flask import session 
from uuid import uuid4 
from datetime import datetime 



def check_verified_purchase(product_id):
    check_verified_purchase = db_creation.confirm_order_collection.find_one({"email":session['email'], "product_id":product_id})
    if check_verified_purchase:
        return True 
    else:
        return False
def add_review(review_message,product_id,rating):
    check_doc_available = db_creation.product_review_collection.find_one({"email":session['email'], "product_id":product_id})
    if check_doc_available ==None :
            schema = {
        "review_id": str(uuid4()) ,
        "email":session['email'],
        "product_id": product_id ,
            "rating": rating , 
        "comment": review_message,
        "created_at": datetime.now(),
        "updated_at": None , 
        "helpful_count": 0, 
        "verified_purchase": check_verified_purchase(product_id),
        #   "status": String,
        #   "images": [String], // Optional, list of image URLs attached to the review
        "response":[ ]
        }

            ins = db_creation.product_review_collection.insert_one(schema)
            if ins.inserted_id:
                return ({"status":True ,"message":f"review update dsuccessfully- {ins.inserted_id}"})
    else :
            return ({"status":False ,"warning":"review aldredy added!  only you can update it if needed"})
            
def add_reply_message(product_id, message, repling_person):
      message = {     
            "message": message ,
            "responded_at": datetime.now() ,
            "user_email":session['email'], 
            "helpful_count":0
        }
      check_review = db_creation.product_review_collection.find_one({"email":repling_person,"product_id":product_id})
      if check_review == None:
           return ({"status":False ,"warning":"no revire find with the user for this product"})
      else :
           check_reply_exists = db_creation.product_review_collection.find_one({"email":repling_person,"product_id":product_id,"response.user_email":session['email']})
           if check_reply_exists == None :
                upd = db_creation.product_review_collection.update_one({"email":repling_person,"product_id":product_id},{"$push":{"response":message}})
                if upd.modified_count ==1:
                        return ({"status":True ,"message":"reply message updated"})
                else :
                        return ({"status":False ,"warning":"something went wrong try again later"})
           else :
                return ({"success":False ,"message":"aldredy reply added! just update the existing"})


#update review 
#update nested review 

def view_all_review_user():
    return 



def view_all_review_product():
    return 



def view_specific_review():
    return 



def edit_review():
    return 


def delete_specific_review():
    return 




def delete_all_review():
    return 


# like an review 



# like an nested review
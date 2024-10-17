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


def update_review(product_id , updated_message ):
     
    upd =  check_review_existance = db_creation.product_review_collection.update_one({"email":session['email'],"product_id":product_id},{"$set":{"comment":updated_message}})
    if upd.modified_count ==1:
         return ({"status":True ,"message":"old review has been updated"})
    else:
         return ({"status":False ,"warning":"some thing went wrong"})


def update_reply_review(product_id,target_email, updated_message): 
    check_reply_found = db_creation.product_review_collection.find_one({"email":target_email, "product_id":product_id,"response.user_email":session['email']})
    if check_reply_found :
         upd = db_creation.product_review_collection.update_one({"email":target_email, "product_id":product_id,"response.user_email":session['email']},{"$set":{"response.$.message":updated_message}})
         if upd.modified_count == 1:
              return ({"status":True , "message":"nested reply has been updated"})
         
         else:
              return ({"status":False ,"message":"reply not updated"})
    else :
         return ({"status":False ,"message":"no replyy found with this account"})



def view_all_review_user(user_email):
    reply = list(db_creation.product_review_collection.find({"email":user_email},{'comment':1,'_id':0}))
    return  reply 



def view_all_review_product(product_id):
    reply = list(db_creation.product_review_collection.find({"product_id":product_id},{'_id':0, "comment":1}))
    return reply



def view_specific_review(review_id):
    qwery={"review_id":review_id}
    print(qwery)
    review_data = db_creation.product_review_collection.find_one(qwery,{"comment":1,'_id':0})
    print(review_data)
    if review_data == None :
         return ({"status":False,"warning":"no review found"})
    else:
         return ({"status":True,"message":review_data})
    

def delete_specific_review(review_id , email):

    delete_check = db_creation.product_review_collection.delete_one({"review_id":review_id, "email":email})
    if delete_check == None :
         return ({"success":False ,"message":"no review found with this id"})
    else :
         return ({"success":True ,"message":"review deleted successfully"})
    




def delete_all_review_user(user_email):
    qwery = {"email":user_email}
    check_review_present = db_creation.product_review_collection.find_one(qwery)
    if check_review_present ==None :
         return ({"status":False ,"message":"this user has np review"})
    else :
         del_all_user_review = db_creation.product_collection.delete_many(qwery)
         if del_all_user_review .deleted_count ==0:
              return ({"success":False, "message":"unable to delete"})
         else :
              return ({"success":True ,"message":"all review from this user has been deleted"})


def delete_all_review_product(product_id ):
     qwery = {"product_id":product_id}
     check_review_presence  = db_creation.product_review_collection.count_documents({"product_id":product_id})
     if check_review_presence >0 :
          return ({"success":False ,"warning":"no product fount with this id"})
     else:
          del_data = db_creation.product_review_collection.delete_many(qwery)
          if del_data.deleted_count >0:
               return ({"success":True ,"message":f"product id {product_id} deleted successfully "})
          else :
               return ({"success":False ,"warning":"no data deleted ! please try again later "})
     


def like_an_review(review_id):
     check_review_existnce = db_creation.product_review_collection.find_one({"review_id":review_id})
     if  check_review_existnce == None :
          return ({"success":False ,"message":"no review found"})
     else :
          update_review = db_creation.product_review_collection.update_one({"review_id":review_id,"liked_person":{"$ne":session['email']}},{"$inc":{"helpful_count":1},"$push":{"liked_person":session['email']}})
          
          if update_review.modified_count ==1 :
               return ({"status":True ,"message":"like has been added"})
          else :
               return ({"status":False , "warning":"like not updated , try later"})




def like_an_nested_review(review_id ,replied_email):

    check_reply_and_nested_reply = db_creation.product_review_collection.find_one({"review_id":review_id,"response.user_email":replied_email})
    if check_reply_and_nested_reply == None  :
         return ({"status":False,"message":"no reply found"})
    else :
         
         upd = db_creation.product_review_collection.update_one({"review_id":review_id,"response.user_email":replied_email, "response.liked_persons":{"$ne":session['email']}},{"$inc":{"response.$.helpful_count":1}, "$push":{"response.$.liked_persons":session['email']}})
         if upd.modified_count==1 :
              return ({"status":True , "message":"like has been updated for inner review "})
         else :
              return ({"status":False,"warning":"like not updated"})
# like an nested review
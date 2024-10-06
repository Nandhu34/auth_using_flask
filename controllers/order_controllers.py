from models import db_creation
from flask import request , session 
from datetime import datetime

def success_status_order(product_id):
    product_existance = db_creation.secondary_cart_collection.find_one({"product_id":product_id, "email":session['email']})
    if product_existance ==None :
        return ({"status":False ,"message":"no product found in cart"})
    else :
        product_existance['order_status']=[{"status":"product_placed","date":datetime.now().isoformat()}]
        # product_existance['date_of_order_placed']= datetime.now()
        ins_data = db_creation.confirm_order_collection.insert_one(product_existance)
        ins_id = ins_data.inserted_id
        if ins_id :
            db_creation.secondary_cart_collection.delete_one({"email":session['email'],"product_id":product_id})
            return ({"success":True,"message":f"product with product-id {ins_id} is successfully placed"})
        else :
            return ({"status":False ,"message":"network error try again later"})
            

def view_confirm_order(page_no):
    limit = 5
    start = (int(page_no)-1)*limit
    limit = start + limit 
    print(start , limit )
    order_details = list(db_creation.confirm_order_collection.find({"email":session['email']}).skip(start).limit(limit))
    for each_data in order_details:
        each_data['_id']= str(each_data['_id'])
    if len(order_details) ==0:
        return ({"success":True ,"warning":"no data found"})
    else :
        return ({"success":True,"length":len(order_details),"data":order_details})


def delete_conform_order(order_id):
    check_data = db_creation.confirm_order_collection.find_one({"email":session['email'],"product_id":order_id})
    if check_data ==None :
        return ({"success":True ,"message":"order id not found"})
    else :
        del_data = db_creation.confirm_order_collection.delete_one({"email":session['email'],"product_id":order_id})
        if del_data.deleted_count==1:
            return ({"success":True, "message":f"order with id {order_id} has been cancelled"})
        else :
            return ({"success":False,"message":"something went wrong, try later"})
        
def track_order(order_id):
    check_data = db_creation.confirm_order_collection.find_one({"email":session['email'],"product_id":order_id})
    if check_data ==None :
        return ({"success":True ,"message":"order id not found"})
    else :
        find_data = db_creation.confirm_order_collection.find_one({"email":session['email'],"product_id":order_id})
        print(find_data)
        return ({"data":find_data['order_status']})
    
    
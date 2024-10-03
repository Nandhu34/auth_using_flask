from flask import session
from controllers import cart_contollers
from models import db_creation
from bson import ObjectId

def add_to_cart(product_id, quantity):
    old_quantity = 10 
    if quantity ==0 :
        quantity = 1
    check_product_presence = db_creation.product_collection.find_one({"_id":ObjectId(product_id)})
    if check_product_presence== None :
        return ({"status":"succeess","data":"no product found in product collection"})
    check_user_presence = db_creation.new_user_collection.find_one({"email":session['email']})
    if check_user_presence == None :
        return ({"status":"success","data":"no user  has been registered"})
    
    check_user_doc_in_cart = db_creation.cart_collection.find_one({"email":session['email']})
    if check_user_doc_in_cart == None :
        document_sample = {"email":session['email'] ,"cart_details":[{"_id":ObjectId(product_id),"quantity":quantity}]} 
        print(document_sample)
        db_creation.cart_collection.insert_one(document_sample)
        print(document_sample['cart_details'])
        document_sample['cart_details'][0]['_id']=str(document_sample['cart_details'][0]['_id'])
        document_sample['_id']=str(document_sample['_id'])
        print(type(document_sample['cart_details'][0]['_id']))
        print(document_sample)
        return ({"data":document_sample})
    else :
        
        return ({"data":"hello"})

    if product_data == None :
        return ({"success":True ,"message":"no product fount with the product id "})
    cart_data = {"user_id"}
    check_product_existance = db_creation.cart_collection.find_one({"product_id":ObjectId(product_id),"email":session['email']})
    if check_product_existance :
        db_creation.cart_collection.update_one({"_id":check_product_existance['_id']},{"$inc":{"quantity":quantity}})
    else :
        cart_data = {"email":session['email'], "product_id":product_id, }


def view_cart():
    return ({"data":"view_cart"})

def update_cart():
    return ({"data":"update cart "})

def delete_cart():
    return ({})
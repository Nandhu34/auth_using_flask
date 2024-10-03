from flask import session
from controllers import cart_contollers
from models import db_creation
from bson import ObjectId

def add_to_cart(product_id, quantity):
    old_quantity = 10 
    if quantity ==0 :
        quantity = 1

    product_data= db_creation.product_collection.find_one({"_id":ObjectId(product_id)})
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
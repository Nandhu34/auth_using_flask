from flask import session , request 
from models import db_creation
from bson import ObjectId

def get_product_data(product_id):
   
   result_data = db_creation.product_collection.find_one({"_id":ObjectId(product_id)})
   print(result_data)
   return result_data
def search_result(data):

    if data.get('product_id'):
        result_data = get_product_data(data['product_id'])
        if result_data:
            result_data['_id'] = str(result_data['_id'])
            return {"success": True, "data": result_data}
        else:
            return {"success": False, "data": "no data found"}

    if data.get('cart_id'):
            result_data = db_creation.secondary_cart_collection.find_one(
                {"email": session['email'], "product_id": data.get('cart_id')}
            )
            if result_data:
                result_data = get_product_data(data['cart_id'])
                result_data['_id'] = str(result_data['_id'])
                return {"success": True, "data": result_data}
            else:
                return {"success": False, "data": "no data found"}

    if data.get('wishlist_id'):
        result_data = db_creation.wishlist_collection.find_one(
            {"email": session['email'], "wishlist_product": ObjectId(data.get('wishlist_id'))}
        )
        if result_data:
            result_data = get_product_data(data['wishlist_id'])
            result_data['_id'] = str(result_data['_id'])
            return {"success": True, "data": result_data}
        else:
            return {"success": False, "data": "no data found"}

    if data.get('confirm_order_id'):
        result_data = db_creation.confirm_order_collection.find_one(
            {"product_id": data['confirm_order_id']}
        )
        if result_data:
            result_data = get_product_data(data['confirm_order_id'])
            result_data['_id'] = str(result_data['_id'])
            return {"success": True, "data": result_data}
        else:
            return {"success": False, "data": "no data found"}

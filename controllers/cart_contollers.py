from flask import session
# from controllers import cart_contollers
from models import db_creation
from bson import ObjectId
from helpers  import paggination



def add_to_cart(product_id, quantity):
    old_quantity = 10 
    if quantity ==0 :
        quantity = 1
    #check product collection 
    check_product_presence = db_creation.product_collection.find_one({"_id":ObjectId(product_id)})
    if check_product_presence== None :
        return ({"status":"succeess","data":"no product found in product collection"})
    # check user collection
    check_user_presence = db_creation.new_user_collection.find_one({"email":session['email']})
    if check_user_presence == None :
        return ({"status":"success","data":"no user  has been registered"})
    check_user_presence_in_primary_collection = db_creation.cart_collection.find_one({"email":session['email']})
    if check_user_presence_in_primary_collection == None :
        new_data_in_primary_collection = db_creation.cart_collection.insert_one({"email":session['email']})
        cart_id = new_data_in_primary_collection.inserted_id
        # print(cart_id)
        # return ({"new data ":str(cart_id)})
    else:
        existance_data_in_primary_collection = db_creation.cart_collection.find_one({"email":session['email']})
        cart_id = str(existance_data_in_primary_collection['_id'])
        # return ({"old data":cart_id})
    print(session['email'])
    check_product_existance_in_secondary_collection = db_creation.secondary_cart_collection.find_one({"email":session['email'],"cart_id":cart_id, "product_id":product_id})
    print(check_product_existance_in_secondary_collection)
    if check_product_existance_in_secondary_collection == None :
        new_data= {"email":session['email'], "cart_id":cart_id,"product_id":product_id,"quantity":quantity}
        db_creation.secondary_cart_collection.insert_one(new_data)
        return ({"status":True ,"message":f"product {product_id} with quantity {quantity} inserted into new doc"})
    else:
        return ({"status":True, "message":"product aldredy in cart"})
        db_creation.secondary_cart_collection.update_one({"email":session['email'],"cart_id":cart_id,"product_id":product_id},{"$set":{"quantity":quantity}})
        return ({"status":True ,"message":f"product {product_id} with quantity {quantity} updated into doc"})


def view_cart(page_no):
    page_limit = 10 
    start = (int(page_no)-1)*10 
    limit = start + page_limit
    
    cart_data = list(db_creation.secondary_cart_collection.find({"email":session['email']}).skip(start).limit(limit))
    len_of_cart = len(cart_data)
    if len_of_cart ==0 :
        return ({"status":False,"message":"no data found"})
    print(cart_data)
    new_doc_for_return = []
    for each_data in cart_data :
        prod_id = each_data['product_id']
        quantity = each_data['quantity']
        product_data = db_creation.product_collection.find_one({"_id":ObjectId(prod_id)})

        product_data['quantity']= quantity
        product_data['_id']= str(product_data['_id'])
        new_doc_for_return.append(product_data)

    

    return ({"data":new_doc_for_return,"length":len(new_doc_for_return)})


def update_cart(quan, prod_id):
    upd = db_creation.secondary_cart_collection.update_one({"product_id":prod_id,"email":session['email']},{"$set":{"quantity":quan}})
    if upd.modified_count==1:

        return ({"status":True,"message":f"{prod_id} with {quan} has been updated "})
    else:
        return ({"status":False,"message":f"{prod_id}  has no updated "})

def delete_cart(product_id):
    deleted_ = db_creation.secondary_cart_collection.delete_one({"product_id":product_id})

    if deleted_.deleted_count ==1 :
        return ({"success":True , "message":f"{product_id} deleted successfully"})
    else :
        return ({"success":False ,"message":f"{product_id} not found"})
    

def view_all_cart_by_user(page_no):
        start , end = paggination.pagination_setup(page_no)
        aggregate_qwery = [
    {
        '$group': {
            '_id': '$email', 
            'cart_id': {
                '$first': '$cart_id'
            }, 
            'total_product_id': {
                '$addToSet': {
                    'product_id': {
                        '$toObjectId': '$product_id'
                    }, 
                    'quantity': '$quantity'
                }
            }
        }
    }, {
        '$unwind': {
            'path': '$total_product_id'
        }
    }, {
        '$lookup': {
            'from': 'product_details', 
            'localField': 'total_product_id.product_id', 
            'foreignField': '_id', 
            'as': 'data'
        }
    }, {
        '$unwind': {
            'path': '$data'
        }
    }, {
        '$addFields': {
            'data._id': {
                '$toString': '$data._id'
            }
        }
    }, {
        '$replaceRoot': {
            'newRoot': {
                '_id': '$_id', 
                'cart_id': '$cart_id', 
                'product_id': {
                    '$toString': '$total_product_id.product_id'
                }, 
                'quantity': '$total_product_id.quantity', 
                'data': '$data'
            }
        }
    }, {
        '$skip': start
    }, {
        '$limit': end
    }
]    
        print(aggregate_qwery)
        aggregate_result = list(db_creation.secondary_cart_collection.aggregate(aggregate_qwery))
        print(aggregate_result)
        if aggregate_result ==0 :
            return ({"status":False,"warning":"no data found from any user"})
        else:
            return ({"success":True ,"message":aggregate_result})

        


def view_all_cart_by_product(page_no):
    start,end = paggination.pagination_setup(page_no)
    aggregation_qwery_to_get_all_products = [
    {
        '$group': {
            '_id': {
                '$toObjectId': '$product_id'
            }, 
            'cart_id': {
                '$first': '$cart_id'
            }, 
            'total_email': {
                '$addToSet': {
                    'email': '$email', 
                    'quantity': '$quantity'
                }
            }
        }
    }, {
        '$unwind': {
            'path': '$total_email'
        }
    }, {
        '$lookup': {
            'from': 'product_details', 
            'localField': '_id', 
            'foreignField': '_id', 
            'as': 'data'
        }
    }, {
        '$unwind': {
            'path': '$data'
        }
    }, {
        '$addFields': {
            '_id': {
                '$toString': '$_id'
            }, 
            'data._id': {
                '$toString': '$data._id'
            }
        }
    }, {
        '$replaceRoot': {
            'newRoot': {
                '_id': '$_id', 
                'cart_id': '$cart_id', 
                'email': '$total_email.email', 
                'quantity': '$total_email.quantity', 
                'data': '$data'
            }
        }
    }, {
        '$skip': start
    }, {
        '$limit': end
    }
]
    all_products_detail = list (db_creation.product_review_collection.aggregate(aggregation_qwery_to_get_all_products))
    if len(all_products_detail) ==0 :
        
            return ({"status":False,"warning":"no data found from any user"})
    else:
            print(len(all_products_detail))
            return ({"success":True ,"message":all_products_detail})

        
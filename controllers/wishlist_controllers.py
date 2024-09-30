from  flask import session
from models import db_creation 
from bson import ObjectId
def add_to_wishlist(data ):
  print("email ---->", session['email'])
  access_token = session['data']['access_token']
  user_data = db_creation.new_user_collection.find_one({"access_token":access_token})
  email = user_data['email']
  if user_data ==None :
    return ({"status":"error","message":"no user found"})
  check_product_id = db_creation.product_collection.find_one({"_id":ObjectId(data)})
  if check_product_id == None : 
    return ({"data":"no data found  for this id "})
  update_wishlist = db_creation.product_collection.update_one({"_id":ObjectId(data)},  {"$addToSet": {"wishlist_users": user_data['email']}})
  if update_wishlist.modified_count ==1:

          return ({"data":f"product- id {data}  add to wishlist"})
  elif update_wishlist.matched_count == 1:
        return ({"status": "info", "message": f"User ID {email} is already in the wishlist for product ID {data}."}), 200
    
  return ({"status": "error", "message": "Product not found."})


def view_all_wishlist(request_data):
    page_no = request_data.get('page')
    limit = 5
    start = (int(page_no)-1)*limit
    limit = start +limit

    product_details =list( db_creation.product_collection.find({"wishlist_users":session['email']}).skip(start).limit(limit))
    if product_details  ==[]:
        return({"status":"success","data":"no product added in wishlist for this user"})
    for each_id in product_details:
        each_id['_id']= str(each_id['_id'])

    return ({"total_document":len(product_details),"data":product_details})
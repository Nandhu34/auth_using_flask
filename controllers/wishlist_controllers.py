from  flask import session
from models import db_creation 
from bson import ObjectId

def add_to_wishlist(data ):
  #data = product id 
  print("email ---->", session['email'])
  access_token = session['data']['access_token']
  user_data = db_creation.new_user_collection.find_one({"access_token":access_token})
  email = user_data['email']

  if user_data ==None :
    return ({"status":"error","message":"no user found"})
  check_product_id = db_creation.product_collection.find_one({"_id":ObjectId(data)})
  if check_product_id == None : 
    return ({"data":"no data found for this id "})
  # check the data found in wishlist 
  user_available  =db_creation.wishlist_collection.find_one({"email":session['email']})
  print(user_available)
  if user_available !=None :
          update_data_in_wishlit = db_creation.wishlist_collection.update_one({"email":session['email']},  {"$addToSet": {"wishlist_product": ObjectId(data)}})
          if update_data_in_wishlit.modified_count ==1:
              return ({"data":f"product- id {data}  add to old wishlist"})
          else :
              return ({"data":f"product-id {data} is aldredy present in  old wishlist "})
          
  elif user_available ==None :
          update_data_in_wishlit = db_creation.wishlist_collection.insert_one({"email":session['email'],"wishlist_product": [ObjectId(data)]})
          if update_data_in_wishlit.inserted_id:
              return ({"data":f"product- id {data}  add to new  wishlist"})
          else :
              return ({"data":f"product-id {data} is aldredy present in new  wishlist "})
          
       
  return ({"status": "error", "message": "Product not found."})


def view_all_wishlist(request_data):
    page_no = request_data.get('page')
    print(page_no)
    print(session['email'])
    limits = 10
    start = (int(page_no)-1)*limits
    limit = start +limits

    product_details =list( db_creation.wishlist_collection.find({"email":session['email']}))
    print(product_details)

    wishlist_id = product_details[0]['wishlist_product']
    print(wishlist_id)
    qwery={'_id':{'$in':wishlist_id}}
    product_list = list(db_creation.product_collection.find(qwery ).skip(start).limit(limit))
    print(product_list)
    for i in product_list:
      i['_id']=str(i['_id'])

    return ({"total_document":len(product_list),"data":product_list})


def delete_wishlist(product_id):
    # product_id = arg_data.get('product_id')
    print(product_id)
    product_exists = db_creation.wishlist_collection.find_one({"email":session['email'],"wishlist_product":{"$in":[ObjectId(product_id)]}})
    if not product_exists :
        return ({"success":False ,"message":f"{product_id} doesnot found  from wishlist"})
    find_qwery={"email":session['email'],"wishlist_product":{"$in":[ObjectId(product_id)]}}
    print(find_qwery)
    update_qwery={"$pull":{"wishlist_product":ObjectId(product_id)}}
    print(update_qwery)
    upd = db_creation.wishlist_collection.update_one(find_qwery,update_qwery)
    if upd.modified_count ==1 :
        return ({"success":True ,"message":f"{product_id} un subscribed from wishlist"})
    else:
        return ({"success":True ,"message":f"{product_id}  not added in wishlist"})
    



    
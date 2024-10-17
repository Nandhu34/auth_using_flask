from  flask import session
from models import db_creation 
from bson import ObjectId
from helpers import paggination


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
    



def view_all_wishlist_user(page_no):
        limit = 5
        start = (int(page_no) -1)*limit
        end = start + limit 
        new_doc={}
        all_docs=[]
        user_data =list( db_creation.wishlist_collection.find({}))
        for each_data in user_data:
            print(each_data)
            product_id_in_user = each_data['wishlist_product']
            product_details_per_user =  list(db_creation.product_collection.find({"_id":{"$in":product_id_in_user}}))
            for each_doc in product_details_per_user:
                each_doc['_id'] = str(each_doc['_id'])
            new_doc['email']= each_data['email']

            new_doc ['product_data'] = product_details_per_user
            all_docs.append(new_doc)

        print(new_doc)
        return ({"success":True ,"data":all_docs})


def view_all_wishlist_product(page_no ):
      start ,end = paggination.pagination_setup(page_no)
      qwery = [
    {
        '$unwind': {
            'path': '$wishlist_product'
        }
    }, {
        '$lookup': {
            'from': 'product_details', 
            'localField': 'wishlist_product', 
            'foreignField': '_id', 
            'as': 'result'
        }
    }, {
        '$project': {
            'email': 1, 
            'result': {
                '$arrayElemAt': [
                    '$result', 0
                ]
            }
        }
    }, {
        '$skip': start
    }, {
        '$limit': end 
    }

]     
      print(start,end)
      product_data =  list(db_creation.wishlist_collection.aggregate(qwery))
      print(product_data)
      return ({"success":True , "data":str(product_data)})

      '''
      {
        "$project": {
            "email": 1,  # Include the email field from wishlist
            "first_product": {"$arrayElemAt": ["$product_data", 0]},  # Get the first product
            "_id": {"$toString": "$_id"},  # Convert the _id of the wishlist to string
            "product_data": {
                "$map": {
                    "input": "$product_data",
                    "as": "product",
                    "in": {
                        "$mergeObjects": [
                            {"_id": {"$toString": "$$product._id"}},  # Convert product _id to string
                            {"$arrayToObject": {"$map": {
                                "input": {"$objectToArray": "$$product"},
                                "as": "field",
                                "in": {
                                    "k": "$$field.k",  # Keep the original key
                                    "v": {"$cond": {
                                        "if": {"$eq": ["$$field.k", "_id"]},
                                        "then": {"$toString": "$$field.v"},
                                        "else": "$$field.v"
                                    }}
                                }
                            }}}
                        ]
                    }
                }
            }
        }
    }
    
    '''
            
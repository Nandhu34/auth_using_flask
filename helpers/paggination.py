from models import db_creation
from bson import ObjectId
def pagination_setup (page_no):
    limit = 5
    start = (int(page_no)-1)*5
    end = start + limit 
    return (start,end )


def  check_product_quantity_fun(product_id, current_quantity ):
     
    db_quantity = db_creation.product_collection.find_one({"_id":ObjectId(product_id)}, {"product_quantity":1,'_id':0})
    db_quantity = db_quantity['product_quantity']
    print(db_quantity)
    return int(db_quantity)
    # if int(current_quantity) > db_quantity:
    # return db_quantity-int(current_quantity)
    
    # else :
        #  return ({"status":True ,"message":f"{db_quantity-int(current_quantity)} availabe "})
    

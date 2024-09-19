from flask import request , jsonify , session 
from models.aggregation_qweries import home_page_discount_based 
from  models.db_creation import product_collection

def home_controller(req):
    if req == "discount": 
        pass
    if req == "price":
        pass 
    else :
        pass 

    data = list(product_collection.aggregate(home_page_discount_based))
    # data ="jii"

    for each_data in data :
        # print(each_data)
        data_= each_data['data']
        print(len(data_))
        
    

        # each_data['_id'] = str(each_data['_id'])
    return ({"data":"hihi"})
    

    


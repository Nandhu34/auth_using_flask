from flask import request , jsonify , session , abort
from models.aggregation_qweries import home_page_discount_based , home_page_actual_price,home_page_mrp_price,normal_aggregation, get_all_category
from  models.db_creation import product_collection

def home_controller(req):
    if req == "discount": 
        
        data = list(product_collection.aggregate(home_page_discount_based))
        # data ="jii"
        dynamic_doc_creation = {    }
        for each_data in data :
            # print(each_data)
            category = each_data['category']
            data_associated_with_category = each_data['data']
            print(category)
            
            # for each_doc_associated_with_category  in data_associated_with_category:
            #     print(each_doc_associated_with_category)
            #     each_doc_associated_with_category['_id'] = str(each_doc_associated_with_category['_id'])
            # dynamic_doc_creation[category] = data_associated_with_category

    if req == "actual_price":
        data = list(product_collection.aggregate(home_page_actual_price))
        # data ="jii"
        dynamic_doc_creation = {    }
        for each_data in data :
            # print(each_data)
            category = each_data['category']
            data_associated_with_category = each_data['data']
            print(category)
            
            # for each_doc_associated_with_category  in data_associated_with_category:
            #     print(each_doc_associated_with_category)
            #     each_doc_associated_with_category['_id'] = str(each_doc_associated_with_category['_id'])
            # dynamic_doc_creation[category] = data_associated_with_category


    if req =="discount_price":
        data = list(product_collection.aggregate(home_page_discount_based))
        # data ="jii"
        dynamic_doc_creation = {    }
        for each_data in data :
            # print(each_data)
            category = each_data['category']
            data_associated_with_category = each_data['data']
            print(category)
            
            # for each_doc_associated_with_category  in data_associated_with_category:
            #     print(each_doc_associated_with_category)
            #     each_doc_associated_with_category['_id'] = str(each_doc_associated_with_category['_id'])
            # dynamic_doc_creation[category] = data_associated_with_category


    

    else :
        data = list(product_collection.aggregate(normal_aggregation))
        # data ="jii"
        dynamic_doc_creation = {    }
        for each_data in data :
            # print(each_data)
            category = each_data['category']
            data_associated_with_category = each_data['data']
            print(category)
            
            # for each_doc_associated_with_category  in data_associated_with_category:
            #     print(each_doc_associated_with_category)
            #     each_doc_associated_with_category['_id'] = str(each_doc_associated_with_category['_id'])
            # dynamic_doc_creation[category] = data_associated_with_category


        # each_data['_id'] = str(each_data['_id'])
    return ({"data":str(data)})



def category():
    try :
      # raise Exception("This is a test error")
      all_categories = list(product_collection.aggregate(get_all_category))
      
      return ({"status":"success","data":all_categories})
    except Exception as e:
       return  abort(403, description=str(e)) 
        

def get_category(category,sub_category,inner_category,page,limit):
    qwery ={}
    start = (page - 1) * limit
    end = start + limit
    print(start,end)
    # skip_limit = {"skip":start}
    # qwery_limit = {"limit":limit}


    if category:
        if sub_category:
            if inner_category:
                qwery={"category":category,"sub_category":sub_category,"inner_category":inner_category}
            else:
                qwery={"category":category,"sub_category":sub_category}
        else:
            qwery={"category":category}
    else:
        qwery={}
    print(qwery)
    if qwery =={}:
        return ({"message":"no data found for selected option"})
    product_data = list(product_collection.find(qwery).skip(start).limit(limit))
     
    if len(product_data)==0:
        return ({"message":"no data found"})
    for each_data in product_data:
        each_data['_id']=str( each_data['_id'])
    return ({"length":len(product_data),"message":product_data})

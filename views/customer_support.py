# customer support  -  send isssue 
# product_review  - review an product 
# search_functionaliy 
# notification -  
# subscribe 

from flask import Blueprint , request
from controllers import customer_support_controllers 

support = Blueprint('support',__name__)



@support.route('/add_customer_support', methods=['POST'])
def add_customer_support():
    request_data = request.json
    category = request_data.get('category')
    message= request_data.get('message')
    return customer_support_controllers.add_new_support(category,message)




@support.route('/view_all_support', methods=['GET'])
def view_customer_support():    
    return customer_support_controllers.view_all_customer_support()


@support.route('/view_specific_support', methods=['GET'])
def view_specific():   
    request_data = request.json 
    support_id = request_data.get("support_id")
    return customer_support_controllers.view_specific_customer_support(support_id)


@support.route('/update_support_admin', methods=['PUT'])
def update_admin_support():    
    return customer_support_controllers.update_message_from_admin(support_id,admin_status,message_from_admin)


@support.route('/update_support_user', methods=['PUT'])
def update_user_support():    
    return customer_support_controllers.update_the_message_from_user(new_message,support_id)


@support.route('/delete_specific_support', methods=['DELETE'])
def delete_customer_support():    
    return customer_support_controllers.delete_specific_support(support_id)




@support.route('/delete_all_support', methods=['DELETE'])
def delete_all_customer_support():    
    return customer_support_controllers.delete_complete_support()



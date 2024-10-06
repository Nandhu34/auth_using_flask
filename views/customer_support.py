# customer support  -  send isssue 
# product_review  - review an product 
# search_functionaliy 
# notification -  
# subscribe 

from flask import Blueprint


support = Blueprint('support',__name__)



@support.route('/customer_support', methods=['GET'])
def customer_support():
    return 
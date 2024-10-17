from flask import Blueprint ,request
from controllers import order_controllers



order = Blueprint('order',__name__)



@order.route('/success_order',methods=['POST'])
def success_status_order():
    try :
        requested_data = request.json
        product_id = requested_data['product_id']
    except Exception as e:
        return ({"status":False,"message":str(e)})
    
    return order_controllers.success_status_order(product_id)

@order.route('/failure_order',methods=['POST'])
def failure_status_order():
    return ({"success":False,"warning":"payment failure try again later"})
    

@order.route('/view_orders', methods=['GET'])
def view_orders():
    try :
        page_no = request.args.get('page_no')
        if page_no ==None :
                 return ({"status":False,"warning":"str(e),field missing"})
    except Exception as e:
        return ({"status":False,"warning":"str(e),field missing"})
    return order_controllers.view_confirm_order(page_no)

@order.route('/cancel_order/<string:confirm_order_id>',methods=['DELETE'])
def cancel_order(confirm_order_id):

    return order_controllers.delete_conform_order(confirm_order_id)




@order.route('/track_order', methods=['GET'])
def track_order():
    try:
          order_id = request.args.get('order_id')
    except Exception as e:
         return ({"success":False , "warning":f"{str(e)},field arquired "})
    
    return order_controllers.track_order(order_id)




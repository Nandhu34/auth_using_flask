from flask import Blueprint ,request
from controllers import order_controllers



order = Blueprint('order',__name__)



@order.route('/success_order',methods=['POST'])
def success_status_order():
    return "success"

@order.route('/failure_order',methods=['POST'])
def failure_status_order():
    return "failure"

@order.route('/view_orders', methods=['GET'])
def view_orders():
    return "view orders "

@order.route('/cancel_order',methods=['POST'])
def cancel_order():
    return "cancel"



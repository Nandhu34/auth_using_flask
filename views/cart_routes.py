from flask import Blueprint , session ,request , jsonify,abort 
from controllers import cart_contollers
from validation import wishlist_validator



cart = Blueprint('cart',__name__)


@cart.route('/add',methods=['POST'])
def add_to_cart():
    request_data  = request.json
    product_id = request_data['product_id']
    quantity = request_data['quantity']
    print(product_id,quantity)
    return cart_contollers.add_to_cart(product_id,quantity)


@cart.route('/view',methods=['GET'])
def view_cart():
    return ({"data":"view_cart"})

@cart.route('/update_cart', methods=['PUT'])
def update_cart():
    return ({"data":"update cart "})

@cart.route('/remove_cart', methods=['DELETE'])
def delete_cart():
    return ({"data":"delete cart "})
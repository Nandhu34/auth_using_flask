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
    page_no = request.args.get('page_no')
    return cart_contollers.view_cart(page_no)


@cart.route('/update_cart', methods=['PUT'])
def update_cart():
    quantity = request.json
    
    try :
        quan = quantity['quantity']
        prod_id = quantity['product_id']
    except Exception as e:
        print(e)
        return ({"success":False,"data":str(e)})

    return cart_contollers.update_cart(quan, prod_id)

@cart.route('/remove_cart', methods=['DELETE'])
def delete_cart():
    body = request.json 

    try:
        product_id = body['product_id']
    except Exception as e:
        return ({"success":False ,"warning":str(e)})
    
    return cart_contollers.delete_cart(product_id)
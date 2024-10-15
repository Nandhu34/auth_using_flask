from flask import Blueprint , session ,request , jsonify,abort 
from controllers import cart_contollers
from validation import wishlist_validator
# from app  import check_token_and_role
from login_role_middleware import check_token_and_role
cart = Blueprint('cart',__name__)


@cart.route('/add',methods=['POST'])
@check_token_and_role([ 'admin'])
def add_to_cart():
    request_data  = request.json
    product_id = request_data['product_id']
    quantity = request_data['quantity']
    print(product_id,quantity)
    return cart_contollers.add_to_cart(product_id,quantity)


@cart.route('/view',methods=['GET'])
def view_cart():
    page_no = request.args.get('page_no')
    if page_no =='' or page_no ==0:
        page_no =1
        
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



# def apply_role_decorator(role, routes):
#     for route in routes :
#         route_decorated = check_token_and_role(role)(route)
#         print(route, route_decorated)
#         app.add_url_rule(route, view_func=route_decorated)
# apply_role_decorator(['admin'], [add_to_cart, update_cart, delete_cart])
# apply_role_decorator(['user', 'admin'], [view_cart])




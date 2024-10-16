from flask import Blueprint , session ,request , jsonify,abort 
from controllers import cart_contollers
from validation import wishlist_validator
# from app  import check_token_and_role
from login_role_middleware import check_token_and_role
cart = Blueprint('cart',__name__)


@cart.route('/add',methods=['POST'])
@check_token_and_role([ 'user','admin'])
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


@cart.route('/view_all_cart_by_user', methods=['GET'])
def view_all_by_user():
    page_no = request.args.get('page_no')
    return cart_contollers.view_all_cart_by_user(page_no)
    
@cart.route('/view_all_cart_by_product', methods=['GET'])
def view_all_cart_products():
    page_no = request.args.get('page_no')
    return  cart_contollers.view_all_cart_by_product(page_no)


@cart.route('/delete_all_user_cart', methods=['DELETE'])
def delete_all_user_cart():
    user_email = request.json.get('user_email')
    print(user_email)
    return cart_contollers.delete_all_user_cart(user_email)


@cart.route('/delete_all_user_product', methods=['DELETE'])
def delete_all_product_cart():
    product_id = request.json.get('product_id')
    return cart_contollers.delete_all_product_cart(product_id)


@cart.route('/check_product_quantity',methods =['GET'])
def check_product_quantity():
    product_id = request.json.get('product_id')
    current_quantity = request.json.get('current_quantity')
    return cart_contollers.check_product_quantity(product_id, current_quantity)

@cart.route('/update_cart_quantity', methods =["PUT"])
def update_cart_quantity():
    product_id = request.json.get('product_id')
    product_quantity= request.json.get('product_quantity')
    return update_cart_quantity(product_id,product_quantity)

# get  if same product id also if has diff user name then we will  provide different doc 

# def apply_role_decorator(role, routes):
#     for route in routes :
#         route_decorated = check_token_and_role(role)(route)
#         print(route, route_decorated)
#         app.add_url_rule(route, view_func=route_decorated)
# apply_role_decorator(['admin'], [add_to_cart, update_cart, delete_cart])
# apply_role_decorator(['user', 'admin'], [view_cart])






from flask import request , session , Blueprint
from controllers import search_controllers


search = Blueprint('search',__name__)




@search.route('/search', methods=['GET'])
def product_search():
    
      product_id =   request.args.get('product_id')
      cart_id = request.args.get('cart_id')
      wishlist_id = request.args.get('wishlist_id')
      confirm_order_id= request.args.get('confirm_order_id')

      print(product_id)
      print(cart_id)
      print(wishlist_id)
      print(confirm_order_id)
      if product_id :
        return search_controllers.search_result({"product_id":product_id})
      if cart_id:
          return search_controllers.search_result({"cart_id":cart_id})
      if wishlist_id:
          return search_controllers.search_result({"wishlist_id":wishlist_id})
      if confirm_order_id:
          return search_controllers.search_result({"confirm_order_id":confirm_order_id})
      else :
          return ({"success":False , "message":"no functionality available"})
      
      
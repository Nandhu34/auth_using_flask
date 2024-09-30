from flask import Blueprint , session ,request , jsonify,abort 
from controllers import wishlist_controllers
from validation import wishlist_validator

wishlist = Blueprint('wishlist', __name__)

# @wishlist.route('/add/<string:user_id>', methods=['GET'])
@wishlist.route('/add/<string:item_id>', methods=['GET'])  # Correct parameter definition
def add_a_new_data_wishlist(item_id):
    return wishlist_controllers.add_to_wishlist(item_id )



@wishlist.route('/view_wishlist',methods=['GET'])
def view_wishlist():
    return wishlist_controllers.view_all_wishlist()
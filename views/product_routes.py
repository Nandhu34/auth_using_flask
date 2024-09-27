from flask import Blueprint , session ,request , jsonify,abort 
from controllers import product_controllers
from validation import product_validator
product = Blueprint('product', __name__)
@product.route('/product',methods=['POST'])
def home_page():
    
    if 'logged_in' in session and session['logged_in']:
        print(session['logged_in'])
        print(session['data'])
        return jsonify({"data": "I am product page"})
    else:
        return jsonify({"data": "Session expired, please login again"})
    
@product.route('/product_home',methods=["GET"])
def product_home_page():

    data = request.get_json()
    if 'based_on' not  in data:
        abort(403, description="Key 'based_on' is missing") 

    try:
       product_validator.validate_home_product_requests(**data )
       

    except Exception as e:
            abort(403, description=str(e)) 

    return product_controllers.home_controller(data['based_on'])
    # return data

@product.route('/categories',methods=['GET'])
def get_all_category():
      return product_controllers.category()


       
    #    return product_controllers.home_controller()
@product.route('/get_categories', methods=['GET'])
def category():
    category = request.args.get('category')
    sub_category = request.args.get('sub_category')
    inner_category = request.args.get('inner_category')
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)

    print(category,sub_category,inner_category,page,limit)
    return    product_controllers.get_category(category,sub_category,inner_category,page,limit)
    
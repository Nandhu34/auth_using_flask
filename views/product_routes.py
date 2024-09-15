from flask import Blueprint , session 

product = Blueprint('product', __name__)
@product.route('/product',methods=['POST'])
def home_page():
    if session['logged_in']:
             print(session['logged_in'])
             print(session['data'])

             return ({"data":"i am product  page "})
    else:
           return ({"data":"session expired so login again "})
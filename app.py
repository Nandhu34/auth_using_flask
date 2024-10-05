from flask import Flask ,jsonify
from  flask_cors import CORS 
from views.login_routes import authorization 
from views.product_routes import product
from views.wishlist_routes import wishlist
from views.cart_routes import cart 
from views.order_management import order
from flask_mail import Mail,Message
# from views.product_routes import product
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)
mail  = Mail(app)
limiter = Limiter(
    get_remote_address,  # Function to get the client IP address
    app=app,
    # key_func=get_remote_address,  # Function to determine the rate limit key
    default_limits=["200 per day", "50 per hour"]  # Default rate limits
)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nandhakumarselva2000@gmail.com'
app.config['MAIL_PASSWORD'] = 'qrxt eswh wlvh timq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app) 
app.register_blueprint(authorization,url_prefix='/api/auth')
app.register_blueprint(product,url_prefix='/api/v1')
app.register_blueprint(wishlist, url_prefix='/api/v1/wishlist')
app.register_blueprint(cart,url_prefix='/api/v1/cart')
app.register_blueprint(order, url_prefix='/api/v1/orders')

@app.route('/rate_limited_home',methods=['POST'])
@limiter.limit("2 per minute")
def rate_limited_home():
    return ({"data":"rate limited route "})


# middleware 


@app.errorhandler(403)
def key_missing_error(e):
    return jsonify(error="key value missed ", message=str(e.description)), 403
@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error="ratelimit exceeded", message=str(e.description)), 429



def home_route():

    return ({"data":"home Route "})

jwt = JWTManager(app) 
app.config['SECRET_KEY'] = 'jfdfd'

if __name__ == '__main__':
    app.run(debug=True )

    
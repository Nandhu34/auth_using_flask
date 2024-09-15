from flask import Flask 
from  flask_cors import CORS 
from views.login_routes import authorization
from flask_mail import Mail,Message
from views.product_routes import product

from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)
mail  = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nandhakumarselva2000@gmail.com'
app.config['MAIL_PASSWORD'] = 'qrxt eswh wlvh timq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app) 
app.register_blueprint(authorization,url_prefix='/api/auth')
app.register_blueprint(product,url_prefix='/api/v1')

# @app.route('/home',methods=['POST'])
def home_route():
    
    return ({"data":"home Route "})

jwt = JWTManager(app) 
app.config['SECRET_KEY'] = 'jfdfd'

if __name__ == '__main__':
    app.run(debug=True )
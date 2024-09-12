from flask import Flask 
from  flask_cors import CORS 
from views.login_routes import authorization
app = Flask(__name__)
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity, jwt_required, JWTManager
app.register_blueprint(authorization,url_prefix='/api/auth')

jwt = JWTManager(app)


if __name__ == '__main__':
    app.run(debug=True )
from flask import Flask 
from  flask_cors import CORS 
from views.login_routes import authorization
app = Flask(__name__)
app.register_blueprint(authorization,url_prefix='/api/auth')



if __name__ == '__main__':
    app.run(debug=True )
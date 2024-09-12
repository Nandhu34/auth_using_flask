from flask import Flask 
from  flask_cors import CORS 
from views.login_routes import authorization
from flask_mail import Mail,Message


app = Flask(__name__)
mail  = Mail(app)

app.config['MAIL_SERVER']= 'live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'nandhakumarselva2000@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity, jwt_required, JWTManager
app.register_blueprint(authorization,url_prefix='/api/auth')

jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'jfdfd'

if __name__ == '__main__':
    app.run(debug=True )
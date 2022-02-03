from logging import log
from flask import Flask, jsonify, after_this_request, session
from resources.posts import posts
from resources.users import users
import models
from flask_cors import CORS
from flask_login import LoginManager, login_manager
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG=True
PORT=8000

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_APP_SECRET")

app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        user = models.User.get_by_id(user_id)
        return user
    except models.DoesNotExist:
        return None
    
@login_manager.unauthorized_handler
def unathorized():
    return jsonify(
        data={
            'error': 'User not logged in'
        },
        message = "You must be logged in to access this resource",
        status=401
    ), 401

CORS(posts, origins=['http://localhost:3000','https://bromeliad-social-app-frontend.herokuapp.com'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000','https://bromeliad-social-app-frontend.herokuapp.com'], supports_credentials=True)

app.register_blueprint(posts, url_prefix='/')
app.register_blueprint(users, url_prefix='/user')

@app.before_request 
def before_request():
    print("Before request") 
    models.DATABASE.connect()

    @after_this_request 
    def after_request(response):
        print("After request")
        models.DATABASE.close()
        return response 

if os.environ.get('FLASK_ENV') != 'development':
    print('\non heroku!')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
    

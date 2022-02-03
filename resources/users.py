import models
from flask import Blueprint,json, request, jsonify, session
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user,current_user, logout_user
from flask_login.utils import login_required

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def user_resource():
    return "user resource works"

@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()
    
    try: 
        models.User.get(models.User.email == payload['email'])
        return jsonify(
            data={},
            message="A userwith that email already exists",
            status=401
        ),401
    except models.DoesNotExist:
        try:
            models.User.get(models.User.username == payload['username'])
            return jsonify(
                data={},
                message= "A user with the username already exists",
                status=401
            ),401
        except models.DoesNotExist:
            pw_hash = generate_password_hash(payload['password'])
            created_user = models.User.create(
                username = payload['username'],
                email = payload['email'],
                password = pw_hash
            )
            session.permanent = True
            login_user(created_user)
            created_user_dict = model_to_dict(created_user)
            created_user_dict.pop('password')
            return jsonify(
                data=created_user_dict,
                message="Successfully registered user.",
                status=201
            ), 201
    
@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    # payload['username'] = payload['username'].lower()
    
    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        password_is_good = check_password_hash(user_dict['password'], payload['password'])
        if(password_is_good):
            session.permanent = True
            login_user(user)
            user_dict.pop('password')
            
            return jsonify(
                data=user_dict,
                message="Successfully logged in.",
                status=200
            ), 200
        else:
            print("Email is no good")
            return jsonify(
                data={},
                message="Email or password is incorrect",
                status=401
            ), 401
    
    except models.DoesNotExist:
        print('email not found')
        return jsonify(
            data={},
            message="Email or password is incorrect",
            status=401
        ), 401

@users.route('/logged_is_user', methods=['GET'])
def get_logged_in_user():
    print(current_user)
   
    if not current_user.is_authenticated:
        return jsonify(
            data={},
            message="No user is currently logged in.",
            status=401,
        ), 401
        
    else:
        print(f"{current_user.username}")
        user_dict = model_to_dict(current_user)
        user_dict.pop('password')
        
        return jsonify(
            data=user_dict,
            message=f"Currently logged in as {user_dict['email']}.",
            status=200
        ), 200
    
@users.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify(
        data={},
        message="Successfully logged out.",
        status=200
    ), 200
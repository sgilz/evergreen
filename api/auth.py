from flask import Blueprint, redirect, url_for, request, flash, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Users
from . import app
import requests
import jwt
import datetime

auth = Blueprint('auth', __name__)

def token_required(f):  
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None 
        if 'x-access-tokens' in request.headers:  
            token = request.headers['x-access-tokens'] 
        if not token:  
            return jsonify({'message': 'a valid token is missing'})   
        try:  
            data = jwt.decode(token, app.config[app.secret_key]) 
            current_user = Users.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message': 'token is invalid'})  
        return f(current_user, *args,  **kwargs)  
    return decorator 

@app.route('/login', methods=['POST'])  
def login_user(): 
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    user = Users.query.filter_by(username=auth.username).first()
        
    if check_password_hash(user.password, auth.password):  
        token = jwt.encode({'username': user.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@auth.route('/signup', methods=['POST'])
def signup_post():
    data = request.get_json() 

    new_user = Users(first_name=data["first_name"], last_name=data["last_name"], role=data["role"], username=data["username"], password=generate_password_hash(data["password"], method='sha256'))
    new_user.save()

    return jsonify({'message': 'registered successfully'})


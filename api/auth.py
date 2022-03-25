from email.policy import default
from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import Users, Roles
from . import app
import jwt
import datetime

auth_app = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None 
        auth = request.headers["Authorization"]
        if auth and 'Bearer ' in auth and len(auth.split()) == 2:  
            token = auth.split()[1]
        if not token:  
            return make_response(jsonify({'message': 'a valid token is missing'}), 401, {'WWW-Authenticate': 'Bearer realm: "login required"'})   
        try:  
            data = jwt.decode(token, app.config['SECRET_KEY'], ["HS256"]) 
            current_user = Users.query.filter_by(username=data['username']).first()
        except Exception as e:
            print(e)
            return make_response(jsonify({'message': 'token is invalid'}), 401, {'WWW-Authenticate': 'Bearer realm: "login required"'})   
        return f(current_user, *args,  **kwargs)  
    return decorator 

def db_init(*args):
    default_roles = ["admin", "guest"]
    for v in default_roles:
        role = Roles.query.filter_by(name=v).first()
        if not role:
            Roles(name=v).save()
    admin = Users.query.filter_by(username="admin").first()
    if not admin:
        Users(first_name="admin", 
            last_name="admin", 
            role="admin", 
            username="admin", 
            password=generate_password_hash("admin", method='sha256')).save()

@app.before_first_request(db_init)

@auth_app.route('/login', methods=['POST'])  
def login_user(): 
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        return make_response(jsonify({'message': 'Could not verify'}), 401, {'WWW-Authenticate': 'Basic realm: "login required"'})    

    user = Users.query.filter_by(username=auth.username).first()
        
    if check_password_hash(user.password, auth.password):  
        token = jwt.encode({'username': user.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], "HS256")
        return jsonify({'token' : token})

    return make_response('could not verify',  401, {'WWW-Authenticate': 'Basic realm: "login required"'})

@auth_app.route('/signup', methods=['POST'])
def signup_post():
    data = request.get_json() 
    user = Users.query.filter_by(username=data["username"]).first()
    if user:
        return make_response(jsonify({"message": f'Username "{data["username"]}" already exists'}), 400)
    Users(first_name=data["first_name"], 
        last_name=data["last_name"], 
        role="guest", 
        username=data["username"], 
        password=generate_password_hash(data["password"], method='sha256')).save()
    return jsonify({'message': 'Registered successfully'})

@auth_app.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    if current_user.role == "admin":
        users = Users.query.all()
        return jsonify({'users': [u.serialize() for u in users]})
    else:
        return make_response(jsonify({"message": "You are not allowed to performe this operation"}), 401, {'WWW-Authenticate': "Admin login required"})

@auth_app.route('/users/delete', methods=['DELETE'])
@token_required
def delete_user(current_user):
    if current_user.role == "admin":
        data = request.get_json()
        if current_user.username != data["username"]:
            try:
                Users.query.filter_by(username=data["username"]).first().delete()
            except:
                return make_response(jsonify({"message": "Error while deleting user"}), 401, {'WWW-Authenticate': ""})
            return jsonify({'message': f'User "{data["username"]}" deleted successfully'})
        else:
            return make_response(jsonify({"message": "You are not allowed to delete your own user"}), 401, {'WWW-Authenticate': 'Another admin login required"'})
    else:
        return make_response(jsonify({"message": "You are not allowed to performe this operation"}), 401, {'WWW-Authenticate': "Admin login required"})

@auth_app.route('/users/assign', methods=['PATCH'])
@token_required
def assign_role(current_user):
    if current_user.role == "admin":
        data = request.get_json()
        role = Roles.query.filter_by(name=data["role_name"]).first()
        user = Users.query.filter_by(username=data["username"]).first()
        if not (role and user):
            return make_response(jsonify({"message": f'Non existing user or role'}), 400)
        user.role = role.name
        user.save()
        return jsonify({'message': f'Role {data["role_name"]} assigned successfully to user {data["username"]}'})
    else:
        return make_response(jsonify({"message": "You are not allowed to performe this operation"}), 401, {'WWW-Authenticate': "Admin login required"})

@auth_app.route('/roles', methods=['GET'])
@token_required
def get_roles(current_user):
    return jsonify({'roles': [u.serialize() for u in Roles.query.all()]})

@auth_app.route('/roles/create', methods=['POST'])
@token_required
def create_role(current_user):
    if current_user.role == "admin":
        data = request.get_json()
        role = Roles.query.filter_by(name=data["name"]).first()
        if role:
            return make_response(jsonify({"message": f'Role "{data["name"]}" already exists'}), 400)
        Roles(name=data["name"]).save()
        return jsonify({'message': f'Role {data["name"]} registered successfully'})
    else:
        return make_response(jsonify({"message": "You are not allowed to performe this operation"}), 401, {'WWW-Authenticate': "Admin login required"})
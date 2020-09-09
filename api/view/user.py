from flask import request, json, Response, Blueprint, abort
from flask_jwt_extended import (create_access_token, jwt_required, get_raw_jwt, get_jwt_identity)
from ..model.user import UserModel, UserSchema
from ..model.blacklist_token import BlacklistToken

user_api = Blueprint('users', __name__)
user_schema = UserSchema()

def check_admin():
    admin = get_admin()
    if not admin:
        abort(403)

@user_api.route('/signup', methods=['POST'])
def create_user():
    """Creates user."""
    req_data = request.get_json(force=True)
    data, error = user_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    # check existance of a user
    existing_email = UserModel.get_user_by_email(data.get('email'))
    existing_username = UserModel.get_user_by_username(data.get('username'))
    if existing_email:
        message = {'error':'User with this email already exist if it is you. Go on and log in, if not provide another email and try again'}
        return custom_response(message, 400)
    if existing_username:
        message = {'error':'User with this username already exist if it is you. Go on and log in, if not provide another username and try again'}
        return custom_response(message, 400)
    
    if 'is_provider' in data:
        data['is_provider'] = True

    user = UserModel(data)
    user.save()
    user_ser_data = user_schema.dump(user).data
    token = create_access_token(user_ser_data.get('id'))
    return custom_response({'meassage': 'User successfully created!', 'token': token}, 201)

@user_api.route('/auth/signin', methods=['POST'])
def signin_user():
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)

    if error:
        return custom_response(error, 400)

    if not data.get('email'):
        return custom_response({'error': 'You need email or password to sign in'}, 400)

    if not data.get('password'):
        return custom_response({'error': 'You need email or password to sign in'}, 400)

    user = UserModel.get_user_by_email(data.get('email'))

    if not user:
        return custom_response({'error': 'Invalid email or password!'}, 400)

    if not user.check_password_hash(data.get('password')):
        return custom_response({'error': 'Invalid email or password!'}, 400)

    user_ser_data = user_schema.dump(user).data
    token = create_access_token(user_ser_data.get('id'))

    return custom_response({'userdata':user_ser_data, 'token': token}, 200)

@user_api.route('/auth/signout', methods=['POST'])
@jwt_required
def signout_user():
    jti = get_raw_jwt()['jti']
    try:
        blacklist_token = BlacklistToken(jti=jti)
        blacklist_token.add()
        return custom_response({'message': 'You have signedout successfully!'}, 200)
    except:
        return custom_response({'error': 'Something went wrong'}, 500)
    

@user_api.route('/auth/<int:user_id>', methods=['GET'])
@jwt_required
def get_a_user(user_id):

    # Get a single user

    user = UserModel.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)
    
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)

def custom_response(res, status_code):

    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

def get_admin():
    current_user = get_jwt_identity()
    user = UserModel.get_one_user(current_user)
    is_admin = user.is_admin
    return is_admin

def get_provider():
    current_user = get_jwt_identity()
    user = UserModel.get_one_user(current_user)
    return user.is_provider

def check_provider():
    provider = get_provider()
    if not provider:
        abort(403)

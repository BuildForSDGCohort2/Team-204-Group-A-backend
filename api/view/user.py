from flask import request, json, Response, Blueprint
from ..model.user import UserModel, UserSchema
from ..auth.authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()

@user_api.route('/signup', methods=['POST'])
def create_user():
    """Creates user."""
    req_data = request.get_json()
    data = user_schema.load(req_data)

    # check existance of a user
    existing_email = UserModel.get_user_by_email(data.get('email'))
    existing_username = UserModel.get_user_by_username(data.get('username'))
    if existing_email:
        message = {'error':'User with this email already exist if it is you. Go on and log in, if not provide another email and try again'}
        return custom_response(message, 400)
    if existing_username:
        message = {'error':'User with this username already exist if it is you. Go on and log in, if not provide another username and try again'}
        return custom_response(message, 400)
    

    user = UserModel(data)
    user.save()
    return custom_response({'meassage': 'User successfully created!'}, 201)

@user_api.route('/signin', methods=['POST'])
def signin_user():
    req_data = request.get_json()
    data = user_schema.load(req_data, partial=True)

    if not data.get('username'):
        return custom_response({'error': 'You need username or password to sign in'}, 400)

    if not data.get('password'):
        return custom_response({'error': 'You need username or password to sign in'}, 400)

    user = UserModel.get_user_by_username(data.get('username'))

    if not user:
        return custom_response({'error': 'Invalid username or password!'}, 400)

    if not user.check_password_hash(data.get('password')):
        return custom_response({'error': 'Invalid username or password!'}, 400)

    return custom_response({'message': 'You have successfully sign in!'}, 200)

def custom_response(res, status_code):

    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

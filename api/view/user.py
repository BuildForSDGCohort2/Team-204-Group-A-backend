from flask import request, json, Response, Blueprint
from ..model.user import UserModel, UserSchema
from ..auth.authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()

@user_api.route('/signup', methods=['POST'])
def create_user():
    """
    Creates user
    """

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

def custom_response(res, status_code):

    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

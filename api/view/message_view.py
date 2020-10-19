from flask import request, json, Response, Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..view.user import custom_response
from ..model.message import MessageModel, MessageSchema
from ..model.user import UserModel
import datetime

message_schema = MessageSchema()
message_api = Blueprint('messages', __name__)

@message_api.route('/send_message/<int:recepient_id>', methods=['GET', 'POST'])
@jwt_required
def send_message(recepient_id):
    recepient = UserModel.get_one_user(recepient_id)
    current_user = get_jwt_identity()
    sender = UserModel.get_one_user(current_user)
    req_data = request.get_json(force=True)
    data, error = message_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    msg = data.get('message')
    message = MessageModel(message = msg, author=sender, recipient=recepient, created_at = datetime.datetime.utcnow(), modified_at = datetime.datetime.utcnow())
    message.save()
    return custom_response({'message': 'Message successfully send'}, 201)

@message_api.route('/<int:message_id>', methods=['GET'])
@jwt_required
def get_a_message(message_id):

    # Get a single message

    message = MessageModel.get_one_message(message_id)
    if not message:
        return custom_response({'error': 'message not found'}, 404)
    
    ser_message = message_schema.dump(message).data
    return custom_response(ser_message, 200)

@message_api.route('/', methods=['GET'])
@jwt_required
def get_all_messages():
    messages = MessageModel.get_all_messages()

    if not messages:
        return custom_response({'error': 'messages lists is empty'}, 404)

    ser_messages = message_schema.dump(messages, many=True).data
    return custom_response(ser_messages, 200)

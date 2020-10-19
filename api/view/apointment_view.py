from flask import request, json, Response, Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..view.user import custom_response
from ..model.appointment import AppointmentModel, AppointmentSchema
from ..model.user import UserModel
import datetime

appointment_schema = AppointmentSchema()
appointment_api = Blueprint('appointments', __name__)

@appointment_api.route('/book_appointment/<int:patient_id>', methods=['GET', 'POST'])
@jwt_required
def book_appointment(patient_id):
    patient = UserModel.get_one_user(patient_id)
    current_user = get_jwt_identity()
    provider = UserModel.get_one_user(current_user)
    req_data = request.get_json(force=True)
    data, error = appointment_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    msg = data.get('details')
    details = AppointmentModel(details = msg, provider=provider, patient=patient,
                created_at = datetime.datetime.utcnow(), modified_at = datetime.datetime.utcnow())
    message.save()
    return custom_response({'message': 'Message successfully send'}, 201)

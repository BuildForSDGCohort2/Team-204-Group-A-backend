from flask import request, json, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..model.facility import FacilityModel
from ..model.user import UserModel, UserSchema
from ..view.user import custom_response, check_provider
from .. import db

user_schema = UserSchema()
provider_api = Blueprint('provider', __name__)

@provider_api.route('/assign/facility/<int:facility_id>', methods=['GET', 'POST'])
@jwt_required
def assign_facility(facility_id):

    check_provider()
    
    current_user = get_jwt_identity()
    user = UserModel.get_one_user(current_user)
    facility = FacilityModel.get_one_facility(facility_id)
    user.facility = facility
    db.session.add(user)
    db.session.commit()

    return custom_response({'message':'You are assigned to {}.'.format(facility.facilityname)},201)

@provider_api.route('/<int:facility_id>', methods=['GET'])
@jwt_required
def get_providers_list(facility_id):

    provider = UserModel.get_providers(facility_id)

    if not provider:
        return custom_response({'error': 'Facility lists is empty'}, 404)

    ser_provider = user_schema.dump(provider, many=True).data
    return custom_response(ser_provider, 200)

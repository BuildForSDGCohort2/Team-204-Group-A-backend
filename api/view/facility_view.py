from flask import request, json, Blueprint
from flask_jwt_extended import jwt_required
from ..model.facility import FacilityModel, FacilitySchema
from ..view.user import custom_response, check_admin

facility_api = Blueprint('facilities', __name__)
facility_schema = FacilitySchema()

@facility_api.route('/create', methods=['POST'])
@jwt_required
def create_facility():

    check_admin()
    req_data = request.get_json(force=True)
    data, error = facility_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    # check existance of a facility
    existing_facility = FacilityModel.get_user_by_facility_name(data.get('facilityname'))
    if existing_facility:
        return custom_response({'error': 'This facility already exists.'}, 400)

    facility = FacilityModel(data)
    facility.save()
    return custom_response({'message': 'Facility created successfully'}, 201)

@facility_api.route('/', methods=['GET'])
@jwt_required
def get_all_facilities():
    facilities = FacilityModel.get_all_facilities()

    if not facilities:
        return custom_response({'error': 'Facility lists is empty'}, 404)

    ser_facilities = facility_schema.dump(facilities, many=True).data
    return custom_response(ser_facilities, 200)

@facility_api.route('/<int:facility_id>', methods=['GET'])
@jwt_required
def get_one_facility(facility_id):
    facility = FacilityModel.get_one_facility(facility_id)

    if not facility:
        return custom_response({'error': 'Facility not found contact admin'}, 404)

    ser_facility = facility_schema.dump(facility).data
    return custom_response(ser_facility, 200)

@facility_api.route('/delete/<int:facility_id>', methods=['DELETE'])
@jwt_required
def delete(facility_id):
    check_admin()
    facility = FacilityModel.get_one_facility(facility_id)
    if not facility:
        return custom_response({'error':'facility not found'}, 404)

    facility.delete()
    return custom_response({'message':'Facility deleted!'}, 204)

@facility_api.route('/update/<int:facility_id>', methods=['PUT'])
@jwt_required
def update_facility(facility_id):
    check_admin()
    req_data = request.get_json()
    facility = FacilityModel.get_one_facility(facility_id)
    if not facility:
        return custom_response({'error':'facility not found'}, 404)
    data = facility_schema.dump(facility).data
    data, error = facility_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    facility.update(data)
    data = facility_schema.dump(facility).data
    return custom_response(data, 200)
    
import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

from app.models import Building, Street, Session, Company
from app.controllers.schemas import AddNewBuildingSchema, GetBuildingByIdSchema, UpdateBuildingByIdSchema, \
    DeleteBuildingByIdSchema

add_new_building_schema = AddNewBuildingSchema()
get_building_by_id_schema = GetBuildingByIdSchema()
update_building_by_id_schema = UpdateBuildingByIdSchema()
delete_building_by_id_schema = DeleteBuildingByIdSchema()


def generate_add_building_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'building_id': id})


def generate_delete_building_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'building_id': id})


def generate_building_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_BUILDING_NOT_FOUND, 'Building not found: ' + id))


def generate_company_not_found_error(id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_COMPANY_NOT_FOUND, 'Company not found: ' + id))


def generate_street_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_STREET_NOT_FOUND, 'Street not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_building_schema)
def add_new_building(data):
    uuid = data.get('uuid')
    name = data.get('name')
    company_id = data.get('company_id')
    street_id = data.get('street_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        street = db.session.query(Street).get(street_id)
        if street:
            company = db.session.query(Company).get(company_id)
            if company:
                building = Building(name=name, street_id=street_id, company_id=company_id)
                building.save()
                return generate_add_building_success_response(building.id)
            else:
                return generate_company_not_found_error(id)
        else:
            return generate_street_not_found_error(street_id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_building_by_id_schema)
def get_building_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filer_by(uuid=uuid).first()
    if session:
        building = db.session.query(Building).get(id)
        if building:
            building_dict = building.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'buildingData': building_dict})
        else:
            return generate_building_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_building_by_id_schema)
def update_building_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    name = data.get('name')
    company_id = data.get('company_id')
    street_id = data.get('street_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        street = db.session.query(Street).get(street_id)
        if street:
            company = db.session.query(Company).get(company_id)
            if company:
                building = Building(name=name, street_id=street_id, company_id=company_id)
                if building:
                    building.name = name
                    building.company_id = company_id
                    building.street_id = street_id
                    building.update_building()
                    building_dict = building.to_dict()
                    return jsonify(
                        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                         'error_message': '',
                         'buildingData': building_dict})
                else:
                    return generate_building_not_found_error(id)
            else:
                return generate_company_not_found_error(id)
        else:
            return generate_street_not_found_error(street_id)

    else:
        return generate_user_not_login_response()


@validate_schema(delete_building_by_id_schema)
def delete_building_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        building = db.session.query(Building).get(id)
        if building:
            building.delete_building()
            return generate_delete_building_success_response(id)
        else:
            return generate_building_not_found_error(id)
    else:
        return generate_user_not_login_response()

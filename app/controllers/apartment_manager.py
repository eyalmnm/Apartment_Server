import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

from app.models import Session, Floor, Company, Apartment
from app.controllers.schemas import AddNewApartmentSchema, GetApartmentByIdSchema, UpdateApartmentByIdSchema, \
    DeleteApartmentByIdSchema

add_new_apartment_schema = AddNewApartmentSchema()
get_apartment_by_id_schema = GetApartmentByIdSchema()
update_apartment_by_id_schema = UpdateApartmentByIdSchema()
delete_apartment_by_id_schema = DeleteApartmentByIdSchema()


def generate_add_apartment_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'apartment_id': id})


def generate_delete_apartment_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'apartment_id': id})


def generate_apartment_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_APARTMENT_NOT_FOUND, 'Apartment not found: ' + id))


def generate_floor_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_FLOOR_NOT_FOUND, 'Floor not found: ' + id))


def generate_company_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_COMPANY_NOT_FOUND, 'Company not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_apartment_schema)
def add_new_apartment(data):
    uuid = data.get('uuid')
    name = data.get('name')
    company_id = data.get('company_id')
    floor_id = data.get('floor_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).get(company_id)
        if company:
            floor = db.session.query(Floor).get(floor_id)
            if floor:
                apartment = Apartment(name=name, floor_id=floor_id, company_id=company_id)
                apartment.save()
                return generate_add_apartment_success_response(apartment.id)
            else:
                return generate_floor_not_found_error(floor_id)
        else:
            return generate_company_not_found_error(company_id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_apartment_by_id_schema)
def get_apartment_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        apartment = db.session.query(Apartment).get(id)
        if apartment:
            apartment_dict = apartment.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'apartmenData': apartment_dict})
        else:
            return generate_apartment_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_apartment_by_id_schema)
def update_apartment_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    name = data.get('name')
    company_id = data.get('company_id')
    floor_id = data.get('floor_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).get(company_id)
        if company:
            floor = db.session.query(Floor).get(floor_id)
            if floor:
                apartment = db.session.query(Apartment).get(id)
                apartment.name = name
                apartment.company_id = company_id
                apartment.floor_id = floor_id
                apartment.update_apartment()
                apartment_dict = apartment.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                     'error_message': '',
                     'apartmenData': apartment_dict})
            else:
                return generate_floor_not_found_error(floor_id)
        else:
            return generate_company_not_found_error(company_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_apartment_by_id_schema)
def delete_apartment_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        apartment = db.session.query(Apartment).get(id)
        if apartment:
            apartment.delete_apartment()
            return generate_delete_apartment_success_response(id)
        else:
            return generate_apartment_not_found_error(id)
    else:
        return generate_user_not_login_response()
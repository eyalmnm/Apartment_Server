import json

from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddNewCountrySchema, GetCountryByIdSchema, UpdateCountryByIdSchema, \
    DeleteCountryByIdSchema
from app.models import Country, Session
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_new_country_schema = AddNewCountrySchema()
get_country_by_id_schema = GetCountryByIdSchema()
update_country_by_id_schema = UpdateCountryByIdSchema()
delete_country_by_id_schema = DeleteCountryByIdSchema()


def generate_add_country_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'country_id': id})


def generate_delete_country_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'country_id': id})


def generate_country_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_COUNTRY_NOT_FOUND, 'Country not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_country_schema)
def add_new_country(data):
    uuid = data.get('uuid')
    name = data.get('name')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        country = Country(name=name)
        country.save()
        return generate_add_country_success_response(country.id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_country_by_id_schema)
def get_country_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        country = db.session.query(Country).get(id)
        if country:
            country_dict = country.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'countryData': country_dict})
        else:
            return generate_country_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_country_by_id_schema)
def update_country_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    name = data.get('name')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        country = db.session.query(Country).get(id)
        if country:
            country.name = name
            country.update_country()
            country_dict = country.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'countryData': country_dict})
        else:
            return generate_country_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_country_by_id_schema)
def delete_country_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        country = db.session.query(Country).get(id)
        country.delete_country()
        return generate_delete_country_success_response(country.id)
    else:
        return generate_user_not_login_response()

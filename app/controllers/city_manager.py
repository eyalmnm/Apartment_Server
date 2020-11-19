import json

from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddNewCitySchema, GetCityByIdSchema, UpdateCityByIdSchema, DeleteCityByIdSchema
from app.models import City, Session
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_new_city_schema = AddNewCitySchema()
get_city_by_id_schema = GetCityByIdSchema()
update_city_by_id_schema = UpdateCityByIdSchema()
delete_city_by_id_schema = DeleteCityByIdSchema()


def generate_add_city_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'city_id': id})


def generate_delete_city_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'city_id': id})


def generate_city_not_found_error(id):
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_CITY_NOT_FOUND, 'City not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_city_schema)
def add_new_city(data):
    uuid = data.get('uuid')
    name = data.get('name')
    state_id = data.get('state_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        city = City(name=name, state_id=state_id)
        city.save()
        return generate_add_city_success_response(city.id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_city_by_id_schema)
def get_city_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        city = db.session.query(City).get(id)
        if city:
            city_dict = city.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'cityData': city_dict})
        else:
            return generate_city_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_city_by_id_schema)
def update_city_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    name = data.get('name')
    state_id = data.get('state_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        city = db.session.query(City).get(id)
        if city:
            city.name = name
            city.state_id = state_id
            city.update_city()
            city_dict = city.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'cityData': city_dict})
        else:
            return generate_city_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_city_by_id_schema)
def delete_city_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        city = db.session.query(City).get(id)
        if city:
            city.delete_city()
            return generate_delete_city_success_response(city.id)
        else:
            return generate_city_not_found_error(id)
    else:
        return generate_user_not_login_response()

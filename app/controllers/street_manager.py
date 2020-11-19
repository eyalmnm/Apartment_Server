import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

from app.models import Street, Session
from app.controllers.schemas import AddNewStreetSchema, GetStreetByIdSchema, UpdateStreetByIdSchema, \
    DeleteStreetByIdSchema

add_new_street_schema = AddNewStreetSchema()
get_street_by_id_schema = GetStreetByIdSchema()
update_street_by_id_schema = UpdateStreetByIdSchema()
delete_street_by_id_schema = DeleteStreetByIdSchema()


def generate_add_street_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'street_id': id})


def generate_delete_street_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'street_id': id})


def generate_street_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_STREET_NOT_FOUND, 'Street not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_street_schema)
def add_new_street(data):
    uuid = data.get('uuid')
    city_id = data.get('city_id')
    name = data.get('name')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        street = Street(name=name, city_id=city_id)
        street.save()
        return generate_add_street_success_response(street.id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_street_by_id_schema)
def get_street_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        street = db.session.query(Street).get(id)
        if street:
            street_dict = street.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'streetData': street_dict})
        else:
            return generate_street_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_street_by_id_schema)
def update_street_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    city_id = data.get('city_id')
    name = data.get('name')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        street = db.session.query(Street).get(id)
        if street:
            street.city_id = city_id
            street.name = name
            street.update_street()
            street_dict = street.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'streetData': street_dict})
        else:
            return generate_street_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_street_by_id_schema)
def delete_street_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        street = db.session.query(Street).get(id)
        if street:
            street.delete_street()
            return generate_delete_street_success_response(street.id)
        else:
            return generate_street_not_found_error(id)
    else:
        return generate_user_not_login_response()

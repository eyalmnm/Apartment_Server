import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

from app.models import Building, Session, Entrance
from app.controllers.schemas import AddNewEntranceSchema, GetEntranceByIdSchema, UpdateEntranceByIdSchema, \
    DeleteEntranceByIdSchema

add_new_entrance_schema = AddNewEntranceSchema()
get_entrance_by_id_schema = GetEntranceByIdSchema()
update_entrance_by_id_schema = UpdateEntranceByIdSchema()
delete_entrance_by_id_schema = DeleteEntranceByIdSchema()


def generate_add_entrance_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'entrance_id': id})


def generate_delete_entarnce_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'entrance_id': id})


def generate_entarnce_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_ENTRANCE_NOT_FOUND, 'Entrance not found: ' + id))


def generate_building_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_BUILDING_NOT_FOUND, 'Building not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_entrance_schema)
def add_new_entrance(data):
    uuid = data.get('uuid')
    building_id = data.get('building_id')
    name = data.get('name')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        building = db.session.query(Building).get(building_id)
        if building:
            entrance = Entrance(name=name, building_id=building_id)
            entrance.save()
            return generate_add_entrance_success_response(entrance.id)
        else:
            return generate_building_not_found_error(building_id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_entrance_by_id_schema)
def get_entrance_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        entrance = db.session.query(Entrance).get(id)
        entrance_dict = entrance.to_dict()
        if entrance:
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'entranceData': entrance_dict})
        else:
            return generate_entarnce_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_entrance_by_id_schema)
def update_entrance_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    building_id = data.get('building_id')
    name = data.get('name')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        entrance = db.session.query(Entrance).get(id)
        if entrance:
            entrance.building_id = building_id
            entrance.name = name
            entrance.update_entrance()
            entrance_dict = entrance.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'entranceData': entrance_dict})
        else:
            return generate_entarnce_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_entrance_by_id_schema)
def delete_entrance_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        entrance = db.session.query(Entrance).get(id)
        if entrance:
            entrance.delete_entrance()
            return generate_delete_entarnce_success_response(id)
        else:
            return generate_entarnce_not_found_error(id)
    else:
        return generate_user_not_login_response()

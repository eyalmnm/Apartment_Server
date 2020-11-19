import json

from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddNewStateSchema, GetStateByIdSchema, UpdateStateByIdSchema, DeleteStateByIdSchema
from app.models import State, Session
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_new_state_schema = AddNewStateSchema()
get_state_by_id_schema = GetStateByIdSchema()
update_state_by_id_schema = UpdateStateByIdSchema()
delete_state_by_id_schema = DeleteStateByIdSchema()


def generate_add_state_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'state_id': id})


def generate_delete_state_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'state_id': id})


def generate_state_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_STATE_NOT_FOUND, 'State not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_state_schema)
def add_new_state(data):
    uuid = data.get('uuid')
    country_id = data.get('country_id')
    name = data.get('name')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        state = State(name=name, country_id=country_id)
        state.save()
        return generate_add_state_success_response(state.id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_state_by_id_schema)
def get_state_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        state = db.session.query(State).get(id)
        if state:
            state_dict = state.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'stateData': state_dict})
        else:
            return generate_state_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_state_by_id_schema)
def update_state_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    country_id = data.get('country_id')
    name = data.get('name')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        state = db.session.query(State).get(id)
        if state:
            state.name = name
            state.country_id = country_id
            state.update_state()
            state_dict = state.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'stateData': state_dict})
        else:
            return generate_state_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_state_by_id_schema)
def delete_state_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        state = db.session.query(State).get(id)
        if state:
            state.delete_state()
            return generate_delete_state_success_response(state.id)
        else:
            return generate_state_not_found_error(id)
    else:
        return generate_user_not_login_response()

import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

from app.models import Session, Room, Questionnaire
from app.controllers.schemas import AddNewQuestionnaireSchema, GetQuestionnaireByIdSchema, \
    UpdateQuestionnaireByIdSchema, DeleteQuestionnaireByIdSchema

add_new_questionnaire_schema = AddNewQuestionnaireSchema()
get_questionnaire_by_id_schema = GetQuestionnaireByIdSchema()
update_questionnaire_by_id_schema = UpdateQuestionnaireByIdSchema()
delete_questionnaire_by_id_schema = DeleteQuestionnaireByIdSchema()


def generate_add_questionnaire_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'questionnaire_id': id})


def generate_delete_questionnaire_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'questionnaire_id': id})


def generate_questionnaire_not_found_error(id) -> json:
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_QUESTIONNAIRE_NOT_FOUND, 'Questionnaire not found: ' + id))


def generate_room_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_ROOM_NOT_FOUND, 'Room not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_questionnaire_schema)
def add_new_questionnaire(data):
    uuid = data.get('uuid')
    id = data.get(id)
    name = data.get('name')
    room_id = data.get('room_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        room = db.session.query(Room).get(room_id)
        if room:
            questionnaire = Questionnaire(id=id, name=name, room_id=room_id)
            questionnaire.save()
            return generate_add_questionnaire_success_response(questionnaire.id)
        else:
            return generate_room_not_found_error(room_id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_questionnaire_by_id_schema)
def get_questionnaire_by_id(data):
    uuid = data.get('uuid')
    id = data.get(id)
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        questionnaire = db.session.query(Questionnaire).get(id)
        if questionnaire:
            questionnaire_dict = questionnaire.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'questionnaireData': questionnaire_dict})
        else:
            return generate_questionnaire_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_questionnaire_by_id_schema)
def update_questionnaire_by_id(data):
    uuid = data.get('uuid')
    id = data.get(id)
    name = data.get('name')
    room_id = data.get('room_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        room = db.session.query(Room).get(room_id)
        if room:
            questionnaire = db.session.query(Questionnaire).get(id)
            if questionnaire:
                questionnaire.name = name
                questionnaire.room_id = room_id
                questionnaire.update_questionnaire()
                questionnaire_dict = questionnaire.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                     'error_message': '',
                     'questionnaireData': questionnaire_dict})
            else:
                return generate_questionnaire_not_found_error(id)
        else:
            return generate_room_not_found_error(room_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_questionnaire_by_id_schema)
def delete_questionnaire_by_id(data):
    uuid = data.get('uuid')
    id = data.get(id)
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        questionnaire = db.session.query(Questionnaire).get(id)
        if questionnaire:
            questionnaire.delete_questionnaire()
            return generate_delete_questionnaire_success_response(id)
        else:
            return generate_questionnaire_not_found_error(id)
    else:
        return generate_user_not_login_response()

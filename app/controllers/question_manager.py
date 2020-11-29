import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

from app.models import Session, Questionnaire, Question
from app.controllers.schemas import AddNewQuestionSchema, GetQuestionByIdSchema, UpdateQuestionByIdSchema, \
    DeleteQuestionByIdSchema

# Question Id will be used by UUID insteadof number
# temp_uuid = generate_uuid()

add_new_question_schema = AddNewQuestionSchema()
get_question_by_id_schema = GetQuestionByIdSchema()
update_question_by_id_schema = UpdateQuestionByIdSchema()
delete_question_by_id_schema = DeleteQuestionByIdSchema()


def generate_add_question_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'question_id': id})


def generate_delete_question_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'question_id': id})


def generate_question_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_QUESTION_NOT_FOUND, 'Question not found: ' + id))


def generate_questionnaire_not_found_error(id) -> json:
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_QUESTIONNAIRE_NOT_FOUND, 'Questionnaire not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_question_schema)
def add_new_question(data):
    uuid = data.get('uuid')
    id = data.get('id')
    type = data.get('type')
    text = data.get('text')
    questionnaire_id = data.get('questionnaire_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        questionnaire = db.session.query(Questionnaire).get(questionnaire_id)
        if questionnaire:
            question = Question(id=id, question_type=type, text=text, questionnaire_uuid=questionnaire_id)
            question.save()
            return generate_add_question_success_response(question.id)
        else:
            return generate_questionnaire_not_found_error(questionnaire_id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_question_by_id_schema)
def get_question_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        question = db.session.query(Question).get(id)
        if question:
            question_dict = question.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'questionData': question_dict})
        else:
            return generate_question_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_question_by_id_schema)
def update_question_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    type = data.get('type')
    text = data.get('text')
    questionnaire_id = data.get('questionnaire_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        questionnaire = db.session.query(Questionnaire).get(questionnaire_id)
        if questionnaire:
            question = Question(id=id, question_type=type, text=text, questionnaire_uuid=questionnaire_id)
            if question:
                question.type = type
                question.text = text
                question.questionnaire_uuid = questionnaire_id
                question.update_question()
                question_dict = question.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                     'error_message': '',
                     'questionData': question_dict})
            else:
                return generate_question_not_found_error(id)
        else:
            return generate_questionnaire_not_found_error(questionnaire_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_question_by_id_schema)
def delete_question_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        question = db.session.query(Question).get(id)
        if question:
            question.delete_question()
            return generate_delete_question_success_response(id)
        else:
            return generate_question_not_found_error(id)
    else:
        return generate_user_not_login_response()

import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

from app.models import Session, Question, Answer
from app.controllers.schemas import AddNewAnswerSchema, GetAnswerByIdSchema, UpdateAnswerByIdSchema, \
    DeleteAnswerByIdSchema

add_new_answer_schema = AddNewAnswerSchema()
get_answer_by_id_schema = GetAnswerByIdSchema()
update_answer_by_id_schema = UpdateAnswerByIdSchema()
delete_answer_by_id_schema = DeleteAnswerByIdSchema()


def generate_add_answer_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'answer_id': id})


def generate_delete_answer_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'answer_id': id})


def generate_answer_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_ANSWER_NOT_FOUND, 'Answer not found: ' + id))


def generate_question_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_QUESTION_NOT_FOUND, 'Question not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_answer_schema)
def add_new_answer(data):
    uuid = data.get('uuid')
    id = data.get('id')
    text = data.get('text')
    question_id = data.get('question_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        question = db.session.query(Question).get(question_id)
        if question:
            answer = Answer(text=text, question_uuid=question_id, id=id)
            answer.save()
            return generate_add_answer_success_response(answer.id)
        else:
            return generate_question_not_found_error(question_id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_answer_by_id_schema)
def get_answer_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        answer = db.session.query(Answer).get(id)
        if answer:
            answer_dict = answer.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'answerData': answer_dict})
        else:
            return generate_answer_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_answer_by_id_schema)
def update_answer_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    text = data.get('text')
    question_id = data.get('question_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        question = db.session.query(Question).get(question_id)
        if question:
            answer = db.session.query(Answer).get(id)
            answer.text = text
            answer.question_uuid = question_id
            answer.update_answer()
            answer_dict = answer.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'answerData': answer_dict})
        else:
            return generate_question_not_found_error(question_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_answer_by_id_schema)
def delete_answer_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        answer = db.session.query(Answer).get(id)
        if answer:
            answer.delete_answer()
            return generate_delete_answer_success_response(id)
        else:
            return generate_answer_not_found_error(id)
    else:
        return generate_user_not_login_response()

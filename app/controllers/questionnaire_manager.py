import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema
from datetime import datetime
from app.utils.uuid_utils import generate_uuid

from app.models import Session, Room, Questionnaire, Item, Question, Answer
from app.controllers.schemas import AddNewQuestionnaireSchema, GetQuestionnaireByIdSchema, \
    UpdateQuestionnaireByIdSchema, DeleteQuestionnaireByIdSchema, UploadFilledQuestionnaireSchema

add_new_questionnaire_schema = AddNewQuestionnaireSchema()
upload_filled_questionnaire_schema = UploadFilledQuestionnaireSchema()
get_questionnaire_by_id_schema = GetQuestionnaireByIdSchema()
update_questionnaire_by_id_schema = UpdateQuestionnaireByIdSchema()
delete_questionnaire_by_id_schema = DeleteQuestionnaireByIdSchema()


def generate_add_questionnaire_success_response(uuid) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'questionnaire_uuid': uuid})


def generate_delete_questionnaire_success_response(uuid) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'questionnaire_uuid': uuid})


def generate_questionnaire_not_found_error(uuid) -> json:
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_QUESTIONNAIRE_NOT_FOUND, 'Questionnaire not found: ' + uuid))


def generate_room_not_found_error(uuid) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_ROOM_NOT_FOUND, 'Room not found: ' + uuid))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_questionnaire_schema)
def add_new_questionnaire(data):
    uuid = data.get('uuid')
    name = data.get('name')
    room_uuid = data.get('room_uuid')
    score = data.get('score')
    date_time = datetime.utcnow()
    temp_uuid = generate_uuid()
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        room = db.session.query(Room).filter_by(uuid=room_uuid).first()
        if room:
            questionnaire = Questionnaire(uuid=temp_uuid, name=name, room_uuid=room_uuid, date_time=date_time, score=score)
            questionnaire.save()
            return generate_add_questionnaire_success_response(questionnaire.uuid)
        else:
            return generate_room_not_found_error(room_uuid)
    else:
        return generate_user_not_login_response()


@validate_schema(upload_filled_questionnaire_schema)
def upload_filled_questionnaire(data):
    ques_counter = 0
    answ_counter = 0
    uuid = data.get('uuid')
    name = data.get('name')
    room_uuid = data.get('room_uuid')
    questionnaire_items = data.get('items')
    date_time = datetime.utcnow()
    questionnaire_uuid = generate_uuid()
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        room = db.session.query(Room).filter_by(uuid=room_uuid).first()
        if room:
            questionnaire = Questionnaire(uuid=questionnaire_uuid, name=name, room_uuid=room_uuid, date_time=date_time, score=0)
            if len(questionnaire_items) > 0:
                for an_item in questionnaire_items:
                    item_uuid = generate_uuid()
                    item_questions = an_item.get('questions')
                    a_item = Item(item_uuid, an_item.get('name'), an_item.get('type'), questionnaire_uuid, date_time)
                    if len(item_questions) > 0:
                        for a_question in item_questions:
                            ques_counter += 1
                            question_uuid = generate_uuid()
                            question_answers = a_question.get('answers')
                            question = Question(question_uuid, a_question.get('type'), a_question.get('text'), item_uuid, date_time)
                            if len(question_answers) > 0:
                                for an_answer in question_answers:
                                    answ_counter += 1
                                    answer_uuid = generate_uuid()
                                    answer = Answer(an_answer.get('text'), question_uuid, answer_uuid, date_time)
                                    answer.save()
                            question.save()
                    a_item.save()
            score = calcScore(ques_counter, answ_counter)
            questionnaire.save()
            return generate_add_questionnaire_success_response(questionnaire.uuid)
        else:
            return generate_room_not_found_error(room_uuid)
    else:
        return generate_user_not_login_response()




@validate_schema(get_questionnaire_by_id_schema)
def get_questionnaire_by_id(data):
    uuid = data.get('uuid')
    questionnaire_uuid = data.get(id)
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        questionnaire = db.session.query(Questionnaire).filter_by(questionnaire_uuid).first()
        if questionnaire:
            questionnaire_dict = questionnaire.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'questionnaireData': questionnaire_dict})
        else:
            return generate_questionnaire_not_found_error(questionnaire_uuid)
    else:
        return generate_user_not_login_response()


@validate_schema(update_questionnaire_by_id_schema)
def update_questionnaire_by_id(data):
    uuid = data.get('uuid')
    questionnaire_uuid = data.get('questionnaire_uuid')
    name = data.get('name')
    room_id = data.get('room_id')
    score = data.get('score')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        room = db.session.query(Room).get(room_id)
        if room:
            questionnaire = db.session.query(Questionnaire).filter_by(uuid=questionnaire_uuid).first()
            if questionnaire:
                questionnaire.name = name
                questionnaire.room_id = room_id
                questionnaire.score = score
                questionnaire.update_questionnaire()
                questionnaire_dict = questionnaire.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                     'error_message': '',
                     'questionnaireData': questionnaire_dict})
            else:
                return generate_questionnaire_not_found_error(questionnaire_uuid)
        else:
            return generate_room_not_found_error(room_id)
    else:
        return generate_user_not_login_response()


def update_questionnaire_score(questionnaire_uuid: str, score: int) -> json:
    questionnaire = db.session.query(Questionnaire).filter_by(uuid=questionnaire_uuid).first()
    if questionnaire:
        questionnaire.score = score
        questionnaire.update_questionnaire()
        questionnaire_dict = questionnaire.to_dict()
        return jsonify(
            {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
             'error_message': '',
             'questionnaireData': questionnaire_dict})
    else:
        return generate_questionnaire_not_found_error(questionnaire_uuid)


@validate_schema(delete_questionnaire_by_id_schema)
def delete_questionnaire_by_id(data):
    uuid = data.get('uuid')
    questionnaire_uuid = data.get('questionnaire_uuid')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        questionnaire = db.session.query(Questionnaire).filter_by('questionnaire_uuid').first()
        if questionnaire:
            questionnaire.delete_questionnaire()
            return generate_delete_questionnaire_success_response(questionnaire_uuid)
        else:
            return generate_questionnaire_not_found_error(questionnaire_uuid)
    else:
        return generate_user_not_login_response()


def score_calculator(questionnaire: Questionnaire) -> int:
    questions_counter: float = 0.0
    answers_counter: float = 0.0
    for item in questionnaire.items:
        for question in item.questions:
            questions_counter += 1
            answers_counter += len(question.answers)
    res = 1.0 - (answers_counter / questions_counter)
    return int(res * 100)


def calcScore(ques_counter, answ_counter):
    res = 1.0 - (answ_counter / ques_counter)
    return int(res * 100)


import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema
from datetime import datetime
from app.utils.uuid_utils import generate_uuid

from app.models import Session, Questionnaire, Item
from app.controllers.schemas import AddNewItemSchema, GetItemByIdSchema, UpdateItemByUuidSchema, DeleteItemByIdSchema

add_new_item_schema = AddNewItemSchema()
get_item_by_id_schema = GetItemByIdSchema()
update_item_by_uuid_schema = UpdateItemByUuidSchema()
delete_item_by_id_schema = DeleteItemByIdSchema()


def generate_add_item_success_response(uuid: str) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'item_uuid': uuid})


def generate_get_item_response(item_dict: dict) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'itemData': item_dict})


def generate_delete_item_success_response(uuid: str) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'item_uuid': uuid})


def generate_item_updated_successfully_response(item_dict: dict) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'itemData': item_dict})


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


def generate_item_not_found_response(uuid: str) -> json:
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_ITEM_NOT_FOUND, 'Item not found: ' + uuid))


def generate_questionnaire_not_found_error(uuid: str) -> json:
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_QUESTIONNAIRE_NOT_FOUND, 'Questionnaire not found: ' + uuid))


@validate_schema(add_new_item_schema)
def add_new_item(data):
    uuid = data.get('uuid')
    name = data.get('name')
    item_type = data.get('type')
    questionnaire_uuid = data.get('questionnaire_uuid')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        questionnaire = db.session.query(Questionnaire).filter_by(uuid=questionnaire_uuid).first()
        if questionnaire:
            temp_uuid = generate_uuid()
            now = datetime.utcnow()
            item = Item(temp_uuid, name, item_type, questionnaire_uuid, now)
            item.save()
            return generate_add_item_success_response(item.uuid)
        else:
            return generate_questionnaire_not_found_error(questionnaire_uuid)
    else:
        return generate_user_not_login_response()


@validate_schema(get_item_by_id_schema)
def get_item_by_id(data):
    uuid = data.get('uuid')
    item_uuid = data.get('item_uuid')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        item = db.session.query(Item).filter_by(uuid=item_uuid).first()
        if item:
            item_dict = item.to_dict()
            return generate_get_item_response(item_dict)
        else:
            return generate_item_not_found_response(item_uuid)
    else:
        return generate_user_not_login_response()


@validate_schema(update_item_by_uuid_schema)
def update_item_by_uuid(data):
    uuid = data.get('uuid')
    item_uuid = data.get('item_uuid')
    name = data.get('name')
    item_type = data.get('type')
    questionnaire_uuid = data.get('questionnaire_uuid')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        item = db.session.query(Item).filter_by(uuid=item_uuid).first()
        if item:
            item.name = name
            item.type = item_type
            item.questionnaire_uuid = questionnaire_uuid
            item.update_item()
            item_dict = item.to_dict()
            return generate_item_updated_successfully_response(item_dict)
        else:
            generate_item_not_found_response(item_uuid)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_item_by_id_schema)
def delete_item_by_id(data):
    uuid = data.get('uuid')
    item_uuid = data.get('item_uuid')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        item = db.session.query(Item).filter_by(uuid=item_uuid).first()
        if item:
            item.delete_item()
            return generate_delete_item_success_response(item_uuid)
        else:
            generate_item_not_found_response(item_uuid)
    else:
        return generate_user_not_login_response()

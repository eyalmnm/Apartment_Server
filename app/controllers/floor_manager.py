import json
from datetime import datetime
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema
from app.utils.uuid_utils import generate_uuid

from app.models import Session, User, Entrance, Floor, FloorComment
from app.controllers.schemas import AddNewFloorSchema, GetFloorByIdSchema, UpdateFloorByIdSchema, DeleteFloorByIdSchema

add_new_floor_schema = AddNewFloorSchema()
get_floor_by_id_schema = GetFloorByIdSchema()
update_floor_by_id_schema = UpdateFloorByIdSchema()
delete_floor_by_id_schema = DeleteFloorByIdSchema()


def generate_add_floor_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'floor_uuid': id})


def generate_delete_floor_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'floor_id': id})


def generate_floor_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_FLOOR_NOT_FOUND, 'Floor not found: ' + id))


def generate_entrance_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_ENTRANCE_NOT_FOUND, 'Entrance not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


def generate_user_not_found_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_FOUND, 'User not found'))


@validate_schema(add_new_floor_schema)
def add_new_floor(data):
    uuid = data.get('uuid')
    entrance_uuid = data.get('entrance_uuid')
    name = data.get('name')
    company_uuid = data.get('company_uuid')
    project_uuid = data.get('project_uuid')
    building_uuid = data.get('building_uuid')
    order = data.get('order')
    comment = data.get('text')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        user_name = session.username
        user = db.session.query(User).filter_by(username=user_name).first()
        if user:
            entrance = db.session.query(Entrance).filter_by(uuid=entrance_uuid).filter_by(company_uuid=company_uuid). \
                filter_by(project_uuid=project_uuid).filter_by(building_uuid=building_uuid).first()
            if entrance:
                floor_uuid = generate_uuid()
                date_time = datetime.utcnow()
                floor = Floor(floor_uuid, company_uuid, project_uuid, building_uuid, entrance_uuid, name, order)
                if comment:
                    floor_comment = FloorComment(text=comment, parent_uuid=floor_uuid,
                                                 author=user.fullname,
                                                 date_time=date_time)
                    floor_comment.save()
                floor.save()
                return generate_add_floor_success_response(floor.uuid)
            else:
                return generate_entrance_not_found_error(entrance_uuid)
        else:
            return generate_user_not_found_response()
    else:
        return generate_user_not_login_response()


@validate_schema(get_floor_by_id_schema)
def get_floor_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        floor = db.session.query(Floor).get(id)
        if floor:
            floor_dict = floor.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'floorData': floor_dict})
        else:
            return generate_floor_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_floor_by_id_schema)
def update_floor_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    entrance_id = data.get('entrance_id')
    name = data.get('name')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        entrance = db.session.query(Entrance).get(entrance_id)
        if entrance:
            floor = db.session.query(Floor).get(id)
            if floor:
                floor.entrance_id = entrance_id
                floor.name = name
                floor.update_floor()
                floor_dict = floor.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                     'error_message': '',
                     'floorData': floor_dict})
            else:
                return generate_floor_not_found_error(id)
        else:
            return generate_entrance_not_found_error(entrance_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_floor_by_id_schema)
def delete_floor_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        floor = db.session.query(Floor).get(id)
        if floor:
            floor.delete_floor()
            return generate_delete_floor_success_response(id)
        else:
            return generate_floor_not_found_error(id)
    else:
        return generate_user_not_login_response()

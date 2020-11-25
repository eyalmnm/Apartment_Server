import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

from app.models import Session, Apartment, Room
from app.controllers.schemas import AddNewRoomSchema, GetRoomByIdSchema, UpdateRoomByIdSchema, DeleteRoomByIdSchema

add_new_room_schema = AddNewRoomSchema()
get_room_by_id_schema = GetRoomByIdSchema()
update_room_by_id_schema = UpdateRoomByIdSchema()
delete_room_by_id_schema = DeleteRoomByIdSchema()


def generate_add_room_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'room_id': id})


def generate_delete_room_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'room_id': id})


def generate_room_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_ROOM_NOT_FOUND, 'Room not found: ' + id))


def generate_apartment_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_APARTMENT_NOT_FOUND, 'Apartment not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_room_schema)
def add_new_room(data):
    uuid = data.get('uuid')
    name = data.get('name')
    apartment_id = data.get('apartment_id')
    type = data.get('type')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        apartment = db.session.query(Apartment).get(apartment_id)
        if apartment:
            room = Room(name=name, apartment_id=apartment_id, type=type)
            room.save()
            return generate_add_room_success_response(room.id)
        else:
            return generate_apartment_not_found_error(apartment_id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_room_by_id_schema)
def get_room_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        room = db.session.query(Room).get(id)
        if room:
            room_dict = room.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'roomData': room_dict})
        else:
            return generate_room_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_room_by_id_schema)
def update_room_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    name = data.get('name')
    apartment_id = data.get('apartment_id')
    type = data.get('type')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        apartment = db.session.query(Apartment).get(apartment_id)
        if apartment:
            room = db.session.query(Room).get(id)
            if room:
                room.name = name
                room.apartment_id = apartment_id
                room.type = type
                room.update_room()
                room_dict = room.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                     'error_message': '',
                     'roomData': room_dict})
            else:
                return generate_room_not_found_error(id)
        else:
            return generate_apartment_not_found_error(apartment_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_room_by_id_schema)
def delete_room_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        room = db.session.query(Room).get(id)
        if room:
            room.delete_room()
            return generate_delete_room_success_response(id)
        else:
            return generate_room_not_found_error(id)
    else:
        return generate_user_not_login_response()

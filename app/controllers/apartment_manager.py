import json
from datetime import datetime
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema
from app.utils.uuid_utils import generate_uuid

from app.models import Session, User, Floor, Company, Apartment, ApartmentComment, Room, Questionnaire
from app.controllers.schemas import AddNewApartmentSchema, GetApartmentByIdSchema, UpdateApartmentByIdSchema, \
    DeleteApartmentByIdSchema, GetApartmentScoreByIdSchema

add_new_apartment_schema = AddNewApartmentSchema()
get_apartment_by_id_schema = GetApartmentByIdSchema()
update_apartment_by_id_schema = UpdateApartmentByIdSchema()
delete_apartment_by_id_schema = DeleteApartmentByIdSchema()
get_apartment_score_by_id_schema = GetApartmentScoreByIdSchema()


def generate_add_apartment_success_response(uuid) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'apartment_uuid': uuid})


def generate_delete_apartment_success_response(uuid) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'apartment_uuid': uuid})


def generate_apartment_score(id, score) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'apartment': id, 'score': score})


def generate_apartment_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_APARTMENT_NOT_FOUND, 'Apartment not found: ' + id))


def generate_floor_not_found_error(uuid) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_FLOOR_NOT_FOUND, 'Floor not found: ' + uuid))


def generate_company_not_found_error(uuid) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_COMPANY_NOT_FOUND, 'Company not found: ' + uuid))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


def generate_user_not_found_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_FOUND, 'User not found'))


@validate_schema(add_new_apartment_schema)
def add_new_apartment(data):
    uuid = data.get('uuid')
    name = data.get('name')
    company_uuid = data.get('company_uuid')
    project_uuid = data.get('project_uuid')
    building_uuid = data.get('building_uuid')
    entrance_uuid = data.get('entrance_uuid')
    floor_uuid = data.get('floor_uuid')
    comment = data.get("text")
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        user_name = session.username
        user = db.session.query(User).filter_by(username=user_name).first()
        if user:
            company = db.session.query(Company).filter_by(uuid=company_uuid).first()
            if company:
                floor = db.session.query(Floor).filter_by(uuid=floor_uuid)
                if floor:
                    temp_uuid = generate_uuid()
                    date_time = datetime.utcnow()
                    apartment = Apartment(uuid=temp_uuid, name=name, floor_uuid=floor_uuid, entrance_uuid=entrance_uuid,
                                          building_uuid=building_uuid, project_uuid=project_uuid,
                                          company_uuid=company_uuid)
                    if comment:
                        apartment_comment = ApartmentComment(text=comment, parent_uuid=temp_uuid,
                                                             author=user.fullname,
                                                             date_time=date_time)
                        apartment_comment.save()
                    apartment.save()
                    return generate_add_apartment_success_response(apartment.uuid)
                else:
                    return generate_floor_not_found_error(floor_uuid)
            else:
                return generate_company_not_found_error(company_uuid)
        else:
            return generate_user_not_found_response()
    else:
        return generate_user_not_login_response()


@validate_schema(get_apartment_by_id_schema)
def get_apartment_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        apartment = db.session.query(Apartment).get(id)
        if apartment:
            apartment_dict = apartment.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'apartmenData': apartment_dict})
        else:
            return generate_apartment_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_apartment_by_id_schema)
def update_apartment_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    name = data.get('name')
    company_id = data.get('company_id')
    floor_id = data.get('floor_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).get(company_id)
        if company:
            floor = db.session.query(Floor).get(floor_id)
            if floor:
                apartment = db.session.query(Apartment).get(id)
                apartment.name = name
                apartment.company_id = company_id
                apartment.floor_id = floor_id
                apartment.update_apartment()
                apartment_dict = apartment.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                     'error_message': '',
                     'apartmenData': apartment_dict})
            else:
                return generate_floor_not_found_error(floor_id)
        else:
            return generate_company_not_found_error(company_id)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_apartment_by_id_schema)
def delete_apartment_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        apartment = db.session.query(Apartment).get(id)
        if apartment:
            apartment.delete_apartment()
            return generate_delete_apartment_success_response(id)
        else:
            return generate_apartment_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(get_apartment_score_by_id_schema)
def get_apartment_score_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        apartment = db.session.query(Apartment).get(id)
        if apartment:
            rooms = apartment.rooms
            if len(rooms) > 0:
                counter = 0
                total = 0.0
                for room in rooms:
                    room_uuid = room.uuid
                    questionnaire = db.session.query(Questionnaire).filter_by(room_uuid=id).order_by('date_time desc').first()
                    total = total + questionnaire.score
                    counter = counter + 1
                score = total / counter
                generate_apartment_score(id, score)
            else:
                return generate_apartment_score(id, -1)
        else:
            return generate_apartment_not_found_error(id)
    else:
        return generate_user_not_login_response()
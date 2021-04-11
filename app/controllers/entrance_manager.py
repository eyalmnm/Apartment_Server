import json
from datetime import datetime

from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema
from app.utils.uuid_utils import generate_uuid

from app.models import User, Company, Project, Building, Session, Entrance, EntranceComment
from app.controllers.schemas import AddNewEntranceSchema, AddAllEntrancesSchema, GetEntranceByIdSchema, \
    UpdateEntranceByIdSchema, DeleteEntranceByIdSchema

add_new_entrance_schema = AddNewEntranceSchema()
add_all_entrances_schema = AddAllEntrancesSchema()
get_entrance_by_id_schema = GetEntranceByIdSchema()
update_entrance_by_id_schema = UpdateEntranceByIdSchema()
delete_entrance_by_id_schema = DeleteEntranceByIdSchema()


def generate_add_entrances_to_buildings_success_response(project_data: dict) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '',
                    'project_data': project_data})


def generate_add_entrance_success_response(uuid: str) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'entrance_uuid': uuid})


def generate_delete_entarnce_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'entrance_id': id})


def generate_company_not_found_error(id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_COMPANY_NOT_FOUND, 'Company not found: ' + id))


def generate_project_not_found_error(project_id: str) -> json:
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_PROJECT_NOT_FOUND, 'Project not found: ' + project_id))


def generate_user_not_found_error():
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_FOUND, 'User not found'))


def generate_entrance_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_ENTRANCE_NOT_FOUND, 'Entrance not found: ' + id))


def generate_building_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_BUILDING_NOT_FOUND, 'Building not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_entrance_schema)
def add_new_entrance(data):
    uuid = data.get('uuid')
    company_uuid = data.get('company_uuid')
    project_uuid = data.get('project_uuid')
    building_uuid = data.get('building_uuid')
    name = data.get('name')
    text = data.get('text')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        user_name = session.username
        user = db.session.query(User).filter_by(username=user_name).first()
        if user:
            company = db.session.query(Company).filter_by(uuid=company_uuid).first()
            temp_uuid = generate_uuid()
            if company:
                project = db.session.query(Project).filter_by(project_uuid=project_uuid).first()
                if project:
                    building = db.session.query(Building).filter_by(uuid=building_uuid).first()
                    if building:
                        entrance = Entrance(temp_uuid, name, company_uuid, project_uuid, building_uuid)
                        if not text:
                            comment = EntranceComment(text, temp_uuid, user.fullname)
                            comment.save()

                        entrance.save()
                        return generate_add_entrance_success_response(temp_uuid)
                    else:
                        return generate_building_not_found_error(building_uuid)
                else:
                    return generate_project_not_found_error(project_uuid)
            else:
                return generate_company_not_found_error(company_uuid)
        else:
            return generate_user_not_found_error()
    else:
        return generate_user_not_login_response()


@validate_schema(add_all_entrances_schema)
def add_all_entrances(data):
    uuid = data.get('uuid')
    company_uuid = data.get('company_uuid')
    project_uuid = data.get('project_uuid')
    entrances = data.get('entrances')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).filter_by(uuid=company_uuid).first()
        user_name = session.username
        user = db.session.query(User).filter_by(username=user_name).first()
        if user:
            if company:
                project = db.session.query(Project).filter_by(project_uuid=project_uuid).first()
                if project:
                    for a_entrance in entrances:
                        try:
                            temp_uuid = generate_uuid()
                            date_time = datetime.utcnow()
                            text = a_entrance.get("text")
                            entrance = Entrance(temp_uuid, a_entrance.get("name"), a_entrance.get("company_uuid"),
                                                a_entrance.get("project_uuid"), a_entrance.get("building_uuid"))
                            if not text:
                                comment = EntranceComment(text, temp_uuid, user.fullname, date_time)
                                comment.save()
                            entrance.save()
                        except Exception as err:
                            print(err)
                    project = db.session.query(Project).filter_by(project_uuid=project_uuid).first()
                    project_dict = project.to_dict()

                else:
                    return generate_project_not_found_error(project_uuid)
            else:
                return generate_company_not_found_error(company_uuid)
        else:
            return generate_user_not_found_error()
    else:
        return generate_user_not_login_response()


@validate_schema(get_entrance_by_id_schema)
def get_entrance_by_id(data):
    uuid = data.get('uuid')
    uuid = data.get('uuid')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        entrance = db.session.query(Entrance).filter_by(uuid=uuid).first()
        if entrance:
            entrance_dict = entrance.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'entranceData': entrance_dict})
        else:
            return generate_entrance_not_found_error(id)
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
        building = db.session.query(Building).get(building_id)
        if building:
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
                return generate_entrance_not_found_error(id)
        else:
            return generate_building_not_found_error(building_id)
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
            return generate_entrance_not_found_error(id)
    else:
        return generate_user_not_login_response()

import json
from datetime import datetime

from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddNewBuildingSchema, GetBuildingByIdSchema, UpdateBuildingByIdSchema, \
    DeleteBuildingByIdSchema, GetBuildingsListSchema, AddNewBuildingsToProjectSchema, GetBuildingsByProjectIdSchema
from app.models import Building, Session, Company, Project, BuildingComment, User
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema
from app.utils.uuid_utils import generate_uuid

add_new_building_schema = AddNewBuildingSchema()
add_new_buildings_to_project_schema = AddNewBuildingsToProjectSchema()
get_building_by_id_schema = GetBuildingByIdSchema()
update_building_by_id_schema = UpdateBuildingByIdSchema()
delete_building_by_id_schema = DeleteBuildingByIdSchema()
get_buildings_list_schema = GetBuildingsListSchema()
get_buildings_by_project_id_schema = GetBuildingsByProjectIdSchema()


def generate_add_building_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'building_id': id})


def generate_delete_building_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'building_id': id})


def generate_building_of_project_save_success_response(project_dict: dict) -> json:
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'projectData': project_dict})


def generate_building_not_found_error(building_id) -> json:
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_BUILDING_NOT_FOUND, 'Building not found: ' + building_id))


def generate_buildings_not_found_error() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_BUILDINGS_NOT_FOUND, 'Building not found'))


def generate_company_not_found_error(id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_COMPANY_NOT_FOUND, 'Company not found: ' + id))


def generate_user_not_found_error():
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_FOUND, 'User not found'))


def generate_project_not_found_error(project_id: str) -> json:
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_PROJECT_NOT_FOUND, 'Project not found: ' + project_id))


def generate_street_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_STREET_NOT_FOUND, 'Street not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_building_schema)
def add_new_building(data):
    uuid = data.get('uuid')
    name = data.get('name')
    company_uuid = data.get('company_uuid')
    project_id = data.get('project_uuid')
    address = data.get('address')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).filter_by(uuid=company_uuid).first()
        if company:
            temp_uuid = generate_uuid()
            building = Building(uuid=temp_uuid, name=name, company_id=company_uuid, latitude=latitude,
                                longitude=longitude,
                                project_id=project_id, address=address)
            building.save()
            return generate_add_building_success_response(building.uuid)
        else:
            return generate_company_not_found_error(id)
    else:
        return generate_user_not_login_response()


def save_building(a_building, company_id, project_id, author):
    temp_uuid = generate_uuid()
    date_time = datetime.utcnow()
    name = a_building.get('name')
    latitude = a_building.get('latitude')
    longitude = a_building.get('longitude')
    address = a_building.get('address')
    text = a_building.get('text')
    building = Building(uuid=temp_uuid, name=name, company_id=company_id, project_id=project_id,
                        latitude=latitude, longitude=longitude, address=address)
    if text:
        comment = BuildingComment(text=text, parent_uuid=temp_uuid, author=author, date_time=date_time)
        comment.save()
    building.save()


@validate_schema(add_new_buildings_to_project_schema)
def add_new_buildings_to_project(data):
    uuid = data.get('uuid')
    address = data.get('address')
    company_uuid = data.get('company_uuid')
    project_uuid = data.get('project_uuid')
    name = data.get('name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    text = data.get('text')
    buildings = data.get('buildings')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        user_name = session.username
        user = db.session.query(User).filter_by(username=user_name).first()
        if user:
            company = db.session.query(Company).filter_by(uuid=company_uuid).first()
            if company:
                project = db.session.query(Project).filter_by(project_uuid=project_uuid).first()
                if project:
                    temp_uuid = generate_uuid()
                    date_time = datetime.utcnow()
                    main_building = Building(uuid=temp_uuid, name=name, company_id=company_uuid,
                                             project_id=project_uuid,
                                             latitude=latitude, longitude=longitude, address=address)
                    for building in buildings:
                        save_building(building, company_id=company_uuid, project_id=project_uuid, author=user.fullname)

                    if not text:
                        main_building_comment = BuildingComment(text=text, parent_uuid=temp_uuid, author=user.fullname,
                                                                date_time=date_time)
                        main_building_comment.save()
                    main_building.save()
                    # Re query the project to have all its buildings include the new ones.
                    project = db.session.query(Project).filter_by(project_uuid=project_uuid).first()
                    project_dict = project.to_dict()
                    return generate_building_of_project_save_success_response(project_dict)
                else:
                    return generate_project_not_found_error(project_uuid)
            else:
                return generate_company_not_found_error(company_uuid)
        else:
            return generate_user_not_found_error()
    else:
        return generate_user_not_login_response()


# ***********************************************************************
# *** Currently return all the project without filtering by distance  ***
# ***********************************************************************
# https://stackoverflow.com/questions/7595050/python-sqlalchemy-filter-query-by-great-circle-distance
@validate_schema(get_buildings_list_schema)
def get_buildings_list(data):
    uuid = data.get('uuid')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    company_uuid = data.get('company_id')
    session = db.session.query(Session).filer_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).filer_by(uuid=company_uuid).first()
        if company:
            buildings = db.session.query(Building).filter_by(company_id=company_uuid).all()
            if buildings:
                buildings_list = list()
                for building in buildings:
                    buildings_list.append(building.to_flat_dict())
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                     'error_message': '',
                     'buildingList': buildings_list})
            else:
                return generate_buildings_not_found_error()
        else:
            return generate_company_not_found_error(company_uuid)
    else:
        return generate_user_not_login_response()


@validate_schema(get_buildings_by_project_id_schema)
def get_buildings_by_project_id(data):
    uuid = data.get('uuid')
    company_uuid = data.get('company_uuid')
    project_uuid = data.get('project_uuid')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).filter_by(uuid=company_uuid).first()
        if company:
            project = db.session.query(Project).filter_by(project_uuid=project_uuid).first()
            if project:
                buildings = db.session.query(Building).filter_by(company_id=company_uuid)\
                    .filter_by(project_id=project_uuid).all()
                if buildings:
                    buildings_list = list()
                    for building in buildings:
                        buildings_list.append(building.to_flat_dict())
                    return jsonify(
                        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                         'error_message': '',
                         'buildingList': buildings_list})
                else:
                    return generate_buildings_not_found_error()
            else:
                return generate_project_not_found_error(project_uuid)
        else:
            return generate_company_not_found_error(company_uuid)
    else:
        return generate_user_not_login_response()


@validate_schema(get_building_by_id_schema)
def get_building_by_id(data):
    uuid = data.get('uuid')
    building_uuid = data.get('building_uuid')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        building = db.session.query(Building).filter_by(uuid=building_uuid).first()
        if building:
            building_dict = building.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'buildingData': building_dict})
        else:
            return generate_building_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_building_by_id_schema)
def update_building_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    name = data.get('name')
    company_uuid = data.get('company_id')
    address = data.get('address')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).get(company_uuid)
        if company:
            building = db.session.query(Building).get(id)
            if building:
                building.name = name
                building.company_id = company_uuid
                building.address = address
                building.latitude = latitude
                building.longitude = longitude
                building.update_building()
                building_dict = building.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                     'error_message': '',
                     'buildingData': building_dict})
            else:
                return generate_building_not_found_error(id)
        else:
            return generate_company_not_found_error(company_uuid)
    else:
        return generate_user_not_login_response()


@validate_schema(delete_building_by_id_schema)
def delete_building_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        building = db.session.query(Building).get(id)
        if building:
            building.delete_building()
            return generate_delete_building_success_response(id)
        else:
            return generate_building_not_found_error(id)
    else:
        return generate_user_not_login_response()

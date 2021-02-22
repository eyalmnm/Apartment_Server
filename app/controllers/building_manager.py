import json

from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import AddNewBuildingSchema, GetBuildingByIdSchema, UpdateBuildingByIdSchema, \
    DeleteBuildingByIdSchema, GetBuildingsListSchema
from app.models import Building, Session, Company
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

add_new_building_schema = AddNewBuildingSchema()
get_building_by_id_schema = GetBuildingByIdSchema()
update_building_by_id_schema = UpdateBuildingByIdSchema()
delete_building_by_id_schema = DeleteBuildingByIdSchema()
get_buildings_list_schema = GetBuildingsListSchema()


def generate_add_building_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'building_id': id})


def generate_delete_building_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'building_id': id})


def generate_building_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_BUILDING_NOT_FOUND, 'Building not found: ' + id))


def generate_buildings_not_found_error() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_BUILDINGS_NOT_FOUND, 'Building not found'))


def generate_company_not_found_error(id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_COMPANY_NOT_FOUND, 'Company not found: ' + id))


def generate_street_not_found_error(id) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_STREET_NOT_FOUND, 'Street not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_building_schema)
def add_new_building(data):
    uuid = data.get('uuid')
    name = data.get('name')
    company_uuid = data.get('company_id')
    address = data.get('address')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).filter_by(uuid=company_uuid).first()
        if company:
            building = Building(name=name, company_id=company_uuid, latitude=latitude, longitude=longitude,
                                address=address)
            building.save()
            return generate_add_building_success_response(building.id)
        else:
            return generate_company_not_found_error(id)
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


@validate_schema(get_building_by_id_schema)
def get_building_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filer_by(uuid=uuid).first()
    if session:
        building = db.session.query(Building).get(id)
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

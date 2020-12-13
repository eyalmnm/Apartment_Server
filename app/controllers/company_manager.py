import json

from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import RegisterNewCompanySchema, RegisterNewSubCompanySchema, GetCompanyIyIdSchema, \
    UpdateCompanyByIdSchema, DeleteCompanyByIdSchema
from app.models import Company, Session, User
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema
from app.config.user_status import UserStatus
from app.config.company_status import CompanyStatus
from app.utils.uuid_utils import generate_uuid, get_hash_password

delete_company_by_id_schema = DeleteCompanyByIdSchema()
update_company_by_id_schema = UpdateCompanyByIdSchema()
get_company_by_id_schema = GetCompanyIyIdSchema()
register_new_sub_company_schema = RegisterNewSubCompanySchema()
register_new_company_schema = RegisterNewCompanySchema()


def generate_registration_success_response(id: str) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'company_id': id})


def generate_company_deletion_success_response(id):
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'company_id': id})


def generate_company_not_found_error(id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_COMPANY_NOT_FOUND, 'Company not found: ' + id))


def generate_failed_to_create_company_response(name: str) -> json:
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_FAILED_TO_CREATE_COMPANY, 'Failed to create company: ' + name))


def generate_user_permissions_not_enough():
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_USER_PERMISSIONS_NOT_ENOUGH, 'Username and permissions not enough'))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(register_new_company_schema)
def register_new_company(data):
    uuid = data.get('uuid')
    name = data.get('name')
    registration_id = data.get('registration_id')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    country = data.get('country')
    zip_code = data.get('zip_code')
    phone = data.get('phone')
    company_uuid = generate_uuid()
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        manager_username = session.username
        manager_user = db.session.query(User).filter_by(username=manager_username).first()
        if manager_user.status == UserStatus.SUPER_ADMIN_USER.value or manager_user.status == UserStatus.ADMIN_USER.value:
            company = Company(name=name, registration_id=registration_id, address=address, city=city, state=state,
                              country=country, zip_code=zip_code, phone=phone, status=CompanyStatus.ACTIVE.value,
                              parent_company_id='', uuid=company_uuid)
            company.save()
            if company.uuid:
                return generate_registration_success_response(company.uuid)
            else:
                return generate_failed_to_create_company_response(name)
        else:
            return generate_user_permissions_not_enough()
    else:
        return generate_user_not_login_response()


@validate_schema(register_new_sub_company_schema)
def register_new_sub_company(data):
    uuid = data.get('uuid')
    name = data.get('name')
    registration_id = data.get('registration_id')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    country = data.get('country')
    zip_code = data.get('zip_code')
    phone = data.get('phone')
    parent_company_id = data.get('parent_company_id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        manager_username = session.username
        manager_user = db.session.query(User).filter_by(username=manager_username).first()
        if manager_user.status == UserStatus.SUPER_ADMIN_USER.value or \
                manager_user.status == UserStatus.ADMIN_USER.value:
            company = Company(name=name, registration_id=registration_id, address=address, city=city,
                              state=state, country=country, zip_code=zip_code, phone=phone,
                              parent_company_id=parent_company_id, status=CompanyStatus.ACTIVE.value)
            company.save()
            if company.id:
                company.set_owner(manager_user.id)
                return generate_registration_success_response(company.id)
            else:
                return generate_failed_to_create_company_response(name)
        else:
            return generate_user_permissions_not_enough()
    else:
        return generate_user_not_login_response()


@validate_schema(get_company_by_id_schema)
def get_company_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).get(id)
        if company:
            company_dict = company.to_dict()
            return jsonify(
                {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                 'error_message': '',
                 'companyData': company_dict})
        else:
            return generate_company_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(update_company_by_id_schema)
def update_company_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    name = data.get('name')
    registration_id = data.get('registration_id')
    parent_company_id = data.get('parent_company_id')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    country = data.get('country')
    zip_code = data.get('zip_code')
    phone = data.get('phone')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        manager_username = session.username
        manager_user = db.session.query(User).filter_by(username=manager_username).first()
        if manager_user.status == UserStatus.SUPER_ADMIN_USER.value or \
                manager_user.status == UserStatus.ADMIN_USER.value:
            company = db.session.query(Company).get(id)
            if company:
                company.name = name
                company.registration_id = registration_id
                company.parent_company_id = parent_company_id
                company.address = address
                company.city = city
                company.state = state
                company.country = country
                company.zip_code = zip_code
                company.phone = phone
                company.update_company()
                company_dict = company.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                     'error_message': '',
                     'companyData': company_dict})
            else:
                return generate_company_not_found_error(id)
        else:
            return generate_user_permissions_not_enough()
    else:
        return generate_user_not_login_response()


@validate_schema(delete_company_by_id_schema)
def delete_company_by_id(data):
    uuid = data.get('uuid')
    id = data.get('id')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        manager_username = session.username
        manager_user = db.session.query(User).filter_by(username=manager_username).first()
        if manager_user.status == UserStatus.SUPER_ADMIN_USER.value or \
                manager_user.status == UserStatus.ADMIN_USER.value:
            company = db.session.query(Company).get(id)
            if company:
                company.status = CompanyStatus.DELETED.value
                company.update_company()
                return generate_company_deletion_success_response(company.id)
            else:
                return generate_company_not_found_error(id)
        else:
            return generate_user_permissions_not_enough()
    else:
        return generate_user_not_login_response()

import json
from datetime import datetime

from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.config.user_status import UserStatus
from app.controllers.schemas import AddNewProjectSchema, GetProjectByIdSchema, GetProjectsAroundMeSchema, \
    RemoveContactFromProjectByContactSchema, AddNewContactToProjectByContactSchema
from app.models import Session, Company, User, Project, ProjectComment, Contact, ContactComment
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema
from app.utils.uuid_utils import generate_uuid

add_new_project_schema = AddNewProjectSchema()
get_project_by_id_schema = GetProjectByIdSchema()
get_projects_around_me_schema = GetProjectsAroundMeSchema()
remove_contact_from_project_by_contact_schema = RemoveContactFromProjectByContactSchema()
add_new_contact_to_project_by_contact_schema = AddNewContactToProjectByContactSchema()


def generate_projects_data(projects_list: []) -> json:
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
         'error_message': '',
         'projects': projects_list})


def generate_project_successfully_saved(uuid: str) -> json:
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
         'error_message': '',
         'project_uuid': uuid})


def generate_project_data(project_data: dict) -> json:
    try:
        return jsonify(
            {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
             'error_message': '',
             'project_data': project_data})
    except Exception as ex:
        print(f'Exception thrown when trying to send project data {ex}')


def generate_failed_to_save_project_data(ex):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_FAILED_TO_STORE_PROJECT, 'Failed to store project: ' + ex))


def generate_failed_to_get_projects_data(ex):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_FAILED_TO_GET_PROJECTS, 'Failed to get projects: ' + ex))


def generate_user_permissions_not_enough():
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_USER_PERMISSIONS_NOT_ENOUGH, 'Username and permissions not enough'))


def generate_user_not_found_response():
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_FOUND, 'Username not found'))


def generate_project_not_found_error(project_uuid: str) -> json:
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_PROJECT_NOT_FOUND, 'Project not found: ' + project_uuid))


def generate_company_not_found_error(id):
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_COMPANY_NOT_FOUND, 'Company not found: ' + id))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


def save_new_contact(a_contact, author, company_uuid, date_time, project_uuid):
    temp_uuid = generate_uuid()
    text = a_contact.get('text')
    name = a_contact.get('name')
    company_name = a_contact.get('company_name')
    phone = a_contact.get('phone')
    email = a_contact.get('email')
    position = a_contact.get('position')
    try:
        if not text:
            comment = ContactComment(text=text, parent_uuid=temp_uuid, author=author, date_time=date_time)
            comment.save()
        contact = Contact(uuid=temp_uuid, company_uuid=company_uuid, name=name, position=position,
                          company_name=company_name, phone=phone, email=email, project_uuid=project_uuid)
        contact.save()
    except Exception as ex:
        print(f'Exception thrown when trying to find a user {ex}')


@validate_schema(add_new_project_schema)
def add_new_project(data):
    uuid = data.get('uuid')
    name = data.get('name')
    company_uuid = data.get('company_uuid')
    address = data.get('address')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    comment = data.get('text')
    contacts = data.get('contacts')
    date_time = data.get('date_time')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).filter_by(uuid=company_uuid).first()
        if date_time is None:
            date_time = datetime.utcnow()
        if company:
            manager_username = session.username
            manager_user = db.session.query(User).filter_by(username=manager_username).first()
            if manager_user.status == UserStatus.SUPER_ADMIN_USER.value or \
                    manager_user.status == UserStatus.ADMIN_USER.value:
                temp_uuid = generate_uuid()
                project = Project(name=name, company_id=company_uuid, latitude=latitude, longitude=longitude,
                                  address=address, project_uuid=temp_uuid, date_time=date_time)
                try:
                    for contact in contacts:
                        save_new_contact(contact, manager_user.fullname, company_uuid, date_time, temp_uuid)
                        if not comment:
                            project_comment = ProjectComment(text=comment, parent_uuid=temp_uuid,
                                                             author=manager_user.fullname,
                                                             date_time=date_time)

                            project_comment.save()

                    project.save()
                    return generate_project_successfully_saved(temp_uuid)
                except Exception as ex:
                    return generate_failed_to_save_project_data(ex)
            else:
                return generate_user_permissions_not_enough()
        else:
            return generate_company_not_found_error(id)
    else:
        return generate_user_not_login_response()


@validate_schema(remove_contact_from_project_by_contact_schema)
def remove_contact_from_project_by_contact(data):
    uuid = data.get('uuid')
    company_uuid = data.get('company_uuid')
    project_uuid = data.get('project_uuid')
    a_contact = data.get('contact')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).filter_by(uuid=company_uuid).first()
        if company:
            project = db.session.query(Project).filter_by(project_uuid=project_uuid).first()
            if project:
                contacts = db.session.query(Contact).filter_by(uuid=a_contact.uuid).all()
                for contact in contacts:
                    contact.parent_uuid = ""
                    contact.update_contact()
                project = db.session.query(Project).filter_by(project_uuid=project_uuid).first()
                project_dict = project.to_dict()
                return generate_project_data(project_dict)
            else:
                return generate_project_not_found_error(project_uuid)
        else:
            return generate_company_not_found_error(company_uuid)
    else:
        return generate_user_not_login_response()


@validate_schema(add_new_contact_to_project_by_contact_schema)
def add_new_contact_to_project_by_contact(data):
    uuid = data.get('uuid')
    company_uuid = data.get('company_uuid')
    project_uuid = data.get('project_uuid')
    a_contact = data.get('contact')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        username = session.username
        user = db.session.query(User).filter_by(username=username).first()
        if user:
            company = db.session.query(Company).filter_by(uuid=company_uuid).first()
            if company:
                project = db.session.query(Project).filter_by(project_uuid=project_uuid).first()
                if project:
                    date_time = datetime.utcnow()
                    save_new_contact(a_contact=a_contact, author=user.fullname, company_uuid=company_uuid,
                                     date_time=date_time, project_uuid=project_uuid)
                    project = db.session.query(Project).filter_by(project_uuid=project_uuid).first()
                    project_dict = project.to_dict()
                    return generate_project_data(project_dict)
                else:
                    return generate_project_not_found_error(project_uuid)
            else:
                return generate_company_not_found_error(company_uuid)
        else:
            return generate_user_not_found_response()
    else:
        return generate_user_not_login_response()


@validate_schema(get_project_by_id_schema)
def get_project_by_id(data):
    uuid = data.get('uuid')
    company_uuid = data.get('company_uuid')
    project_uuid = data.get('project_uuid')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).filter_by(uuid=company_uuid).first()
        if company:
            project = db.session.query(Project).filter_by(project_uuid=project_uuid).first()
            if project:
                project_dict = project.to_dict()
                # project_dict['comments'] = getComments(project.project_uuid)  # remove till it fixed
                return generate_project_data(project_dict)
            else:
                return generate_project_not_found_error(project_uuid)
        else:
            return generate_company_not_found_error(company_uuid)
    else:
        return generate_user_not_login_response()


def getComments(project_uuid):
    comments = []
    stored_comments = db.session.query(ProjectComment).filter_by(parent_uuid=project_uuid).all()
    for comment in stored_comments:
        comments.append(comment.to_dict())
    return comments


@validate_schema(get_projects_around_me_schema)
def get_projects_around_me(data):
    uuid = data.get('uuid')
    company_uuid = data.get('company_uuid')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        company = db.session.query(Company).filter_by(uuid=company_uuid).first()
        if company:
            try:
                projects = db.session.query(Project).filter_by(company_id=company_uuid).all()
                projects_list = []
                for project in projects:
                    projects_list.append(project.to_flat_dict())
                return generate_projects_data(projects_list)
            except Exception as ex:
                return generate_failed_to_get_projects_data(ex)
        else:
            return generate_company_not_found_error(company_uuid)
    else:
        return generate_user_not_login_response()

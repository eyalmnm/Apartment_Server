import json

from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.controllers.schemas import LoginSchema, RegistrationSchema
from app.models import User, Session
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema
from app.utils.uuid_utils import check_hash_password, generate_uuid, get_hash_password
from app.config.user_status import UserStatus

# Ref: https://stackoverflow.com/questions/3332991/sqlalchemy-filter-multiple-columns
# Ref: https://stackoverflow.com/a/44702268

registration_schema = RegistrationSchema()
login_schema = LoginSchema()


def generate_login_success_response(temp_uuid) -> json:
    try:
        return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'uuid': temp_uuid})
    except Exception as ex:
        print(ex)


def generate_user_permissions_not_enough():
    return jsonify(
        create_error_response(ErrorCodes.ERROR_CODE_USER_PERMISSIONS_NOT_ENOUGH, 'Username and permissions not enough'))


def generate_login_failed_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_LOGIN_FAILED, 'Username and Password not found'))


def generate_registration_success_response(temp_uuid) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'uuid': temp_uuid})


def generate_registration_failed_response(exe) -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_REGISTRATION_FAILED, 'User registration failed ' + exe))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(login_schema)
def user_login(data) -> json:
    username = data.get('username')
    password = data.get('password')
    company_id = data.get('company_id')
    user = db.session.query(User).filter_by(username=username).filter_by(company_id=company_id).first()
    if user and check_hash_password(user.hash_pwd, user.salt, password):
        temp_uuid = generate_uuid()
        session_old = db.session.query(Session).filter_by(username=username)
        if session_old:
            session_old.delete()
        session = Session(user.username, temp_uuid)
        if session:
            session.save()
        return generate_login_success_response(temp_uuid)
    else:
        return generate_login_failed_response()


@validate_schema(registration_schema)
def register_new_user(data) -> json:
    try:
        uuid = data.get('uuid')
        username = data.get('username')
        password = data.get('password')
        language = data.get('language')
        status = data.get('status')
        company_id = data.get('company_id')
        phone = data.get('phone')
        email = data('email')

        session = db.session.query(Session).filter_by(uuid=uuid).first()
        if session:
            manager_username = session.username
            manager_user = db.session.query(User).filter_by(username=manager_username).first()
            if manager_user.status == UserStatus.SUPER_ADMIN_USER.value or manager_user.status == UserStatus.ADMIN_USER.value:
                salt = generate_uuid()
                hash_pwd = get_hash_password(salt, password)
                user = User(username=username, email=email, phone=phone, hash_pwd=hash_pwd, salt=salt, language=language,
                            status=status, company_id=company_id)
                if user:
                    temp_uuid = generate_uuid()
                    session = Session(username=user.username, uuid=temp_uuid)
                    user.save_with_session(session)
                    return generate_registration_success_response(temp_uuid)
                else:
                    # raise Exception('Failed to create user')
                    exc = Exception('Failed to create user')
                    generate_registration_failed_response(str(exc))
            else:
                return generate_user_permissions_not_enough()
        else:
            return generate_user_not_login_response()

    except Exception as exc:
        print('user user registration failed: ' + str(exc))
        return generate_registration_failed_response(str(exc))
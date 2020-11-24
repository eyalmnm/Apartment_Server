import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema

from app.models import Session, Analytics
from app.controllers.schemas import AddNewAnalyticsSchema

add_new_analytics_schema = AddNewAnalyticsSchema()


def generate_add_analytics_success_response(id) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'analytics_id': id})


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_analytics_schema)
def add_new_analytics(data):
    uuid = data.get('uuid')
    event = data.get('event')
    data = data.get('data')
    session = db.session.query(Session).filter_by(uuid=uuid).first()
    if session:
        analytic = Analytics(event=event, data=data)
        analytic.save()
        return generate_add_analytics_success_response(analytic.id)
    else:
        return generate_user_not_login_response()

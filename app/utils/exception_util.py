from app.config.constants import ErrorCodes, enum_to_string
from app_config import AppConfig


def create_error_response(code, message):
    response = {'result_code': code.value, 'error_message': enum_to_string(code)}

    if AppConfig.ENV is 'DEV':
        if message:
            response["error_details"] = message
        else:
            response["error_details"] = ""

    print("Error: " + response["error_details"])
    return response

import functools
import json

from flask import request, jsonify
from marshmallow import ValidationError

from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response


def validate_schema(schema):

    def inner_schema_validate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            valid = True
            err_str = None
            try:
                data = schema.loads(request.data)
            except ValidationError as err:
                valid = False
                print(
                    {"message": "error validating schema",
                     "request body": json.loads(request.data),
                     "function": func.__name__})
            except Exception as err:
                valid = False
                err_str = str(err)
                print(
                    {"message": "could not parse request body",
                     "request body": request.data,
                     "function": func.__name__})
            if valid is False:
                err_msg = "could not parse request body"
                if err_str:
                    err_msg = err_msg + ": " + err_str
                return jsonify(create_error_response(ErrorCodes.VALIDATE_INPUT_SCHEMA_FAILED, err_msg))

            return func(data, *args, **kwargs)

        return wrapper

    return inner_schema_validate

from enum import Enum


class ErrorCodes(Enum):
    ERROR_CODE_SUCCESS = 0
    VALIDATE_INPUT_SCHEMA_FAILED = 10

    # Login Error codes (100 - 199)
    ERROR_CODE_LOGIN_FAILED = 100
    ERROR_CODE_USER_NOT_LOGGED_IN = 101
    ERROR_CODE_USERNAME_NOT_AVAILABLE = 102
    ERROR_CODE_FAILED_TO_CREATE_USER = 103

    # Registration Error codes (200 - 299)
    ERROR_CODE_REGISTRATION_FAILED = 200
    ERROR_CODE_UNKNOWN_USERNAME = 201
    ERROR_CODE_USER_PERMISSIONS_NOT_ENOUGH = 202

    # Company Error Codes (300 - 399)
    ERROR_CODE_FAILED_TO_CREATE_COMPANY = 300
    ERROR_CODE_COMPANY_NOT_FOUND = 301

    # Country Error Codes (400 - 499)
    ERROR_CODE_COUNTRY_NOT_FOUND = 400

    # State Error Codes (500 - 599)
    ERROR_CODE_STATE_NOT_FOUND = 500

    # City Error Codes (600 - 699)
    ERROR_CODE_CITY_NOT_FOUND = 600

    # Street Error Codes (700 -799)
    ERROR_CODE_STREET_NOT_FOUND = 700

    # Building Error Codes (800 - 899)
    ERROR_CODE_BUILDING_NOT_FOUND = 800

    # Entrance Error Codes (900 - 999)
    ERROR_CODE_ENTRANCE_NOT_FOUND = 900

    # Floor Error Codes (1000 - 1099)
    ERROR_CODE_FLOOR_NOT_FOUND = 1000

    # Apartment Error Codes (1100 - 1199)
    ERROR_CODE_APARTMENT_NOT_FOUND = 1100

    # Room Error Codes (1200 - 1299)
    ERROR_CODE_ROOM_NOT_FOUND = 1200

    # Questionnaire Error Codes (1300 - 1399)
    ERROR_CODE_QUESTIONNAIRE_NOT_FOUND = 1300

    # Question Error Codes (1400 - 1499)
    ERROR_CODE_QUESTION_NOT_FOUND = 1400

    # Answer Error Codes (1500 - 1599)
    ERROR_CODE_ANSWER_NOT_FOUND = 1500


def enum_to_string(enum):
    return enum.name.lower().replace('_', ' ').replace("cant", "can't").capitalize()

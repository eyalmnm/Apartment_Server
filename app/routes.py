from app import app
from flask import request, make_response

from app.controllers.user_manager import register_new_user, user_login
from app.controllers.company_manager import register_new_company, register_new_sub_company, get_company_by_id, \
    update_company_by_id, delete_company_by_id
from app.controllers.country_manager import add_new_country, get_country_by_id, update_country_by_id, \
    delete_country_by_id
from app.controllers.state_manager import add_new_state, get_state_by_id, update_state_by_id, delete_state_by_id
from app.controllers.city_manager import add_new_city, get_city_by_id, update_city_by_id, delete_city_by_id
from app.controllers.street_manager import add_new_street, get_street_by_id, update_street_by_id, delete_street_by_id
from app.controllers.building_manager import add_new_building, get_building_by_id, update_building_by_id, \
    delete_building_by_id
from app.controllers.entrance_manager import add_new_entrance, get_entrance_by_id, update_entrance_by_id, \
    delete_entrance_by_id
from app.controllers.floor_manager import add_new_floor, get_floor_by_id, update_floor_by_id, delete_floor_by_id


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    return 'Welcome To Apartment Evidence'


# ==================================   User  ==================================
@app.route('/register_user', methods=['POST'])
def register_user():
    """
    uuid = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    language = fields.Str(required=False)
    status = fields.Int(required=True, validate=[validate.OneOf([1, 2, 5, 10])])
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    company_id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'uuid': uuid}
    """
    if check_auth_header_secret():
        return register_new_user()
    else:
        return 'Unknown Package'


@app.route('/login', methods=['POST'])
def login():
    """
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    company_id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'uuid': uuid}
    """
    if check_auth_header_secret():
        return user_login()
    else:
        return 'Unknown Package'


# ==================================   Company  ===============================
@app.route('/register_company', methods=['POST'])
def register_company():
    """
    uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    registration_id = fields.Str(required=True)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=False)
    country = fields.Str(required=True)
    zip_code = fields.Int(required=True)
    phone = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'company_id': id}
    """
    if check_auth_header_secret():
        return register_new_company()
    else:
        return 'Unknown Package'


@app.route('/register_sub_company', methods=["POST"])
def register_sub_company():
    """
    uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    registration_id = fields.Str(required=True)
    parent_company_id = fields.Str(required=False)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=False)
    country = fields.Str(required=True)
    zip_code = fields.Int(required=True)
    phone = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'company_id': id}    
    """
    if check_auth_header_secret():
        return register_new_sub_company()
    else:
        return 'Unknown Package'


@app.route('/get_company', methods=["POST", "GET"])
def get_company():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'companyData': company_dict}
    """
    if check_auth_header_secret():
        return get_company_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_company', methods=["PUT"])
def update_company():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    registration_id = fields.Str(required=True)
    parent_company_id = fields.Str(required=True)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=False)
    country = fields.Str(required=True)
    zip_code = fields.Int(required=True)
    phone = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'companyData': company_dict}
    """
    if check_auth_header_secret():
        return update_company_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_company', methods=["DELETE"])
def delete_company():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'company_id': id}
    """
    if check_auth_header_secret():
        return delete_company_by_id()
    else:
        return 'Unknown Package'


# ==================================   Country  ===============================
@app.route('/add_country', methods=["POST"])
def add_country():
    """
    uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'country_id': id}
    """
    if check_auth_header_secret():
        return add_new_country()
    else:
        return 'Unknown Package'


@app.route('/get_country', methods=["GET", "POST"])
def get_country():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'countryData': country_dict}
    """
    if check_auth_header_secret():
        return get_country_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_country', methods=["PUT"])
def update_country():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'countryData': country_dict}
    """
    if check_auth_header_secret():
        return update_country_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_country', methods=["DELETE"])
def delete_country():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'country_id': id}
    """
    if check_auth_header_secret():
        return delete_country_by_id()
    else:
        return 'Unknown Package'


# ==================================   State  =================================
@app.route('/add_state', methods=["POST"])
def add_state():
    """
    uuid = fields.Str(required=True)
    country_id = fields.Int(required=True)
    name = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'state_id': id}
    """
    if check_auth_header_secret():
        return add_new_state()
    else:
        return 'Unknown Package'


@app.route('/get_state', methods=["POST", "GET"])
def get_state():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'stateData': state_dict}
    """
    if check_auth_header_secret():
        return get_state_by_id()
    else:
        return 'Unknown Package'


@app.route('update_state', methods=['PUT'])
def update_state():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    country_id = fields.Int(required=True)
    name = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'stateData': state_dict}
    """
    if check_auth_header_secret():
        return update_state_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_state', methods=['DELETE'])
def delete_state():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'state_id': id}
    """
    if check_auth_header_secret():
        return delete_state_by_id()
    else:
        return 'Unknown Package'


# ==================================   City  ==================================
@app.route('/add_city', methods=['POST'])
def add_city():
    """
    uuid = fields.Str(required=True)
    state_id = fields.Int(required=True)
    name = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'city_id': id}
    """
    if check_auth_header_secret():
        return add_new_city()
    else:
        return 'Unknown Package'


@app.route('/get_city', methods=['GET', 'POST'])
def get_city():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'cityData': city_dict}
    """
    if check_auth_header_secret():
        return get_city_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_city', methods=['PUT'])
def update_city():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    state_id = fields.Int(required=True)
    name = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'cityData': city_dict}    """
    if check_auth_header_secret():
        return update_city_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_city', methods=['DELETE'])
def delete_city():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'city_id': id}
    """
    if check_auth_header_secret():
        return delete_city_by_id()
    else:
        return 'Unknown Package'


# ==================================   Street  ================================
@app.route('/add_street', methods=['POST'])
def add_street():
    """
    uuid = fields.Str(required=True)
    city_id = fields.Int(required=True)
    name = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'street_id': id}
    """
    if check_auth_header_secret():
        return add_new_street()
    else:
        return 'Unknown Package'


@app.route('/get_city', methods=['POST', 'GET'])
def get_street():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'streetData': street_dict}
    """
    if check_auth_header_secret():
        return get_street_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_street', methods=['PUT'])
def update_street():
    """
    uuid = fields.Str(required=True)
    city_id = fields.Int(required=True)
    name = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'streetData': street_dict}
    """
    if check_auth_header_secret():
        return update_street_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_street', methods=['DELETE'])
def delete_street():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'street_id': id}
    """
    if check_auth_header_secret():
        return delete_street_by_id()
    else:
        return 'Unknown Package'


# ==================================   Building  ==============================
@app.route('/add_building', methods=['POST'])
def add_building():
    """
    uuid = fields.Str(required=True)
    street_id = fields.Int(required=True)
    company_id = fields.Int(required=True)
    name = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'building_id': id}
    """
    if check_auth_header_secret():
        return add_new_building()
    else:
        return 'Unknown Package'


@app.route('/get_building', methods=['POST', 'GET'])
def get_building():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'buildingData': building_dict}
    """
    if check_auth_header_secret():
        return get_building_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_building', methods=['PUT'])
def update_building():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    street_id = fields.Int(required=True)
    company_id = fields.Int(required=True)
    name = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'buildingData': building_dict}
    """
    if check_auth_header_secret():
        return update_building_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_building', methods=['DELETE'])
def delete_building():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'building_id': id}
    """
    if check_auth_header_secret():
        return delete_building_by_id()
    else:
        return 'Unknown Package'


# ==================================   Entrance  ==============================
@app.route('/add_entrance', methods=['POST'])
def add_entrance():
    """
    uuid = fields.Str(required=True)
    building_id = fields.Int(required=True)
    name = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'entrance_id': id}
    """
    if check_auth_header_secret():
        return add_new_entrance()
    else:
        return 'Unknown Package'


@app.route('get_entrance', methods=['POST', 'GET'])
def get_entrance():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'entranceData': entrance_dict}
    """
    if check_auth_header_secret():
        return get_entrance_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_entrance', methods=['PUT'])
def update_entrance():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    building_id = fields.Int(required=True)
    name = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'entranceData': entrance_dict}
    """
    if check_auth_header_secret():
        return update_entrance_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_entrance', methods=['DELETE'])
def delete_entrance():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'entrance_id': id}
    """
    if check_auth_header_secret():
        return delete_entrance_by_id()
    else:
        return 'Unknown Package'


# ==================================   Floor  =================================
@app.route('/add_floor', methods=['POST'])
def add_floor():
    """
    uuid = fields.Str(required=True)
    entrance_id = fields.Int(required=True)
    name = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'floor_id': id}
    """
    if check_auth_header_secret():
        return add_new_floor()
    else:
        return 'Unknown Package'


@app.route('/get_floor', methods=['POST', 'GET'])
def get_floor():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'floorData': floor_dict}
    """
    if check_auth_header_secret():
        return get_floor_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_floor', methods=['PUT'])
def update_floor():
    """
    uuid = fields.Str(required=True)
    entrance_id = fields.Int(required=True)
    name = fields.Int(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'floorData': floor_dict}
    """
    if check_auth_header_secret():
        return update_floor_by_id()
    else:
        return 'Unknown Package'

@app.route('/delete_floor', methods=['PUT'])
def delete_floor():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'floor_id': id}
    """
    if check_auth_header_secret():
        return delete_floor_by_id()
    else:
        return 'Unknown Package'

# ==================================   General  ===============================
def check_auth_header_secret():
    """
    Check if the incoming request's header contains our secretr key
    :return: true if it contains
    """
    bearer_header = request.headers.get('Authorization')
    return 'bearer ' + app.config.get('SECRET_KEY') == bearer_header

# You need to call app.run last, as it blocks execution of anything after it until the server is killed.
# Preferably, use the flask run command instead.
# Ref: https://github.com/pallets/flask/issues/2415
# app.run(debug=True, use_debugger=True, use_reloader=False, passthrough_errors=True)

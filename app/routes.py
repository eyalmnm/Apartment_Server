from app import app
from flask import request, make_response

from app.controllers.user_manager import register_new_user, user_login, the_admin_login
from app.controllers.company_manager import register_new_company, register_new_sub_company, get_company_by_id, \
    update_company_by_id, delete_company_by_id
from app.controllers.building_manager import add_new_building, get_building_by_id, update_building_by_id, \
    delete_building_by_id, get_buildings_list, add_new_buildings_to_project
from app.controllers.entrance_manager import add_new_entrance, add_all_entrances, get_entrance_by_id, \
    update_entrance_by_id, \
    delete_entrance_by_id
from app.controllers.floor_manager import add_new_floor, get_floor_by_id, update_floor_by_id, delete_floor_by_id
from app.controllers.apartment_manager import add_new_apartment, get_apartment_by_id, update_apartment_by_id, \
    delete_apartment_by_id
from app.controllers.room_manager import add_new_room, get_room_by_id, update_room_by_id, delete_room_by_id
from app.controllers.questionnaire_manager import add_new_questionnaire, get_questionnaire_by_id, \
    update_questionnaire_by_id, delete_questionnaire_by_id
from app.controllers.item_manager import add_new_item, get_item_by_id, update_item_by_uuid, delete_item_by_id
from app.controllers.question_manager import add_new_question, get_question_by_id, update_question_by_id, \
    delete_question_by_id
from app.controllers.answer_manager import add_new_answer, get_answer_by_id, update_answer_by_id, delete_answer_by_id
from app.controllers.project_manager import add_new_project, get_project_by_id, get_projects_around_me, \
    remove_contact_from_project_by_contact, add_new_contact_to_project_by_contact

from app.controllers.analytics_manager import add_new_analytics


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    return 'Welcome To Apartment Evidence'


# ==================================   User  ==================================
@app.route('/admin_login', methods=['POST'])
def admin_login():
    """
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'uuid': uuid}
    """
    if check_auth_header_secret():
        return the_admin_login()
    else:
        return 'Unknown Package'


@app.route('/register_user', methods=['POST'])
def register_user():
    """
    uuid = fields.Str(required=True)
    fullname = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    language = fields.Str(required=False)
    status = fields.Int(required=True, validate=[validate.OneOf([1, 2, 5, 10])])
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    company_uuid = fields.Str(required=True)
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
    company_uuid = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'uuid': uuid}
    """
    if check_auth_header_secret():
        return user_login()
    else:
        return 'Unknown Package'


# @app.route('/change_password', methods=['POST']) TODO User MUST sent his current password and the new one all together
# @app.route('/change_user_status', methods=['POST']) TODO Only admin user and super admin user can change

# ==================================   Company  ===============================
@app.route('/register_company', methods=['POST'])
def register_company():
    """
    uuid = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    language = fields.Str(required=False)
    status = fields.Int(required=True, validate=[validate.OneOf([1, 2, 5, 10])])
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    company_id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'company_id': uuid}
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


# ==================================   Project  ===============================
@app.route('/add_project', methods=['POST'])
def add_project():
    """
    uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    company_id = fields.Str(required=True)
    latitude = fields.Decimal(required=True)
    longitude = fields.Decimal(required=True)
    comment = fields.Str(required=False)
    contacts = fields.List(fields.Nested(AddProjectContactSchema), required=False)
    :return: {'result_code': 0, 'error_message': '', 'project_uuid': uuid, 'project_id': id}
    """
    if check_auth_header_secret():
        return add_new_project()
    else:
        return 'Unknown Package'


@app.route('/get_project', methods=['GET', 'POST'])
def get_project():
    """
    uuid = fields.Str(required=True)
    company_uuid = fields.Str(required=True)
    project_uuid = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'project_uuid': uuid, 'project': project.dict}
    """
    if check_auth_header_secret():
        return get_project_by_id()
    else:
        return 'Unknown Package'


@app.route('/get_projects', methods=['GET', 'POST'])
def get_projects():
    """
    uuid = fields.Str(required=True)
    company_uuid = fields.Str(required=True)
    latitude = fields.Decimal(required=True)
    longitude = fields.Decimal(required=True)
    :return: {'result_code': 0, 'error_message': '', 'projects': list<project.dict>}
    """
    if check_auth_header_secret():
        return get_projects_around_me()
    else:
        return 'Unknown Package'


@app.route('/remove_contact_from_project', methods=['POST'])
def remove_contact_from_project():
    """
    uuid = fields.Str(required=True)
    company_uuid = fields.Str(required=True)
    project_uuid = fields.Str(required=True)
    contact = fields.Nested(AddProjectContactSchema), required=False)
    :return: {'result_code': 0, 'error_message': '', 'project_uuid': uuid, 'project': project.dict}
    """
    if check_auth_header_secret():
        return remove_contact_from_project_by_contact()
    else:
        return 'Unknown Package'


@app.route('/add_contact_to_project', methods=['POST'])
def add_contact_to_project():
    """
    uuid = fields.Str(required=True)
    company_uuid = fields.Str(required=True)
    project_uuid = fields.Str(required=True)
    contact = fields.Nested(AddProjectContactSchema), required=False)
    :return: {'result_code': 0, 'error_message': '', 'project_uuid': uuid, 'project': project.dict}
    """
    if check_auth_header_secret():
        return add_new_contact_to_project_by_contact()
    else:
        return 'Unknown Package'


# ==================================   Building  ==============================
@app.route('/add_buildings_to_project', methods=['POST'])
def add_buildings_to_project():
    """
    uuid = fields.Str(required=True)
    address = fields.Str(required=True)
    company_id = fields.Str(required=True)
    project_id = fields.Str(required=True)
    name = fields.Str(required=True)
    latitude = fields.Decimal(required=True)
    longitude = fields.Decimal(required=True)
    text = fields.Str(required=False)
    buildings = fields.List(fields.Nested(AddBuildingsToProjectBuildingSchema), required=False)
    :return: {'result_code': 0, 'error_message': '', 'project_uuid': uuid, 'project_id': id}
    """
    if check_auth_header_secret():
        return add_new_buildings_to_project()
    else:
        return 'Unknown Package'


@app.route('/add_building', methods=['POST'])
def add_building():
    """
    uuid = fields.Str(required=True)
    address = fields.Str(required=True)
    company_id = fields.Int(required=True)
    project_id = fields.Str(required=True)
    name = fields.Str(required=True)
    latitude = fields.Decimal(required=True)
    longitude = fields.Decimal(required=True)
    :return: {'result_code': 0, 'error_message': '', 'building_id': id}
    """
    if check_auth_header_secret():
        return add_new_building()
    else:
        return 'Unknown Package'


@app.route('/get_buildings', methods=['GET', 'POST'])
def get_buildings():
    """
    uuid = fields.Str(required=True)
    company_id = fields.Int(required=True)
    latitude = fields.Decimal(required=True)
    longitude = fields.Decimal(required=True)
    :return: {'result_code': 0, 'error_message': '', 'buildingsList': [{Building}]]}
    """
    if check_auth_header_secret():
        return get_buildings_list()
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
    company_uuid = fields.Str(required=True)
    project_uuid = fields.Str(required=True)
    building_id = fields.Int(required=True)
    name = fields.Str(required=True)
    text = fields.Str(required=False)
    :return: {'result_code': 0, 'error_message': '', 'entrance_uuid': uuid}
    """
    if check_auth_header_secret():
        return add_new_entrance()
    else:
        return 'Unknown Package'


@app.route('/add_entrances', methods=['POST'])
def add_entrances():
    """
    uuid = fields.Str(required=True)
    company_uuid = fields.Str(required=True)
    project_uuid = fields.Str(required=True)
    building_uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    text = fields.Str(required=False)
    order = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'project_data': project_dict}
    """
    if check_auth_header_secret():
        return add_all_entrances()
    else:
        return 'Unknown Package'


@app.route('/get_entrance', methods=['POST', 'GET'])
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
    company_uuid = fields.Str(required=True)
    project_uuid = fields.Str(required=True)
    building_uuid = fields.Str(required=True)
    entrance_uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    :return: {'result_code 0, 'error_message': '', 'floor_id': id}
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


# ==================================   Apartment  =============================
@app.route('/add_apartment', methods=['POST'])
def add_apartment():
    """
    uuid = fields.Str(required=True)
    floor_uuid = fields.Str(required=True)
    entrance_uuid = fields.Str(required=True)
    building_uuid = fields.Str(required=True)
    company_uuid = fields.Str(required=True)
    project_uuid = fields.Str(required=True)
    name = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'apartment_id': id}
    """
    if check_auth_header_secret():
        return add_new_apartment()
    else:
        return 'Unknown Package'


@app.route('/get_apartment', methods=['POST', 'GET'])
def get_apartment():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'apartmentData': apartment_dict}
    """
    if check_auth_header_secret():
        return get_apartment_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_apartment', methods=['PUT'])
def upadte_apartment():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    floor_id = fields.Int(required=True)
    company_id = fields.Int(required=True)
    name = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'apartmentData': apartment_dict}
    """
    if check_auth_header_secret():
        return update_apartment_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_apartment', methods=['DELETE'])
def delete_apartment():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'apartment_id': id}
    """
    if check_auth_header_secret():
        return delete_apartment_by_id()
    else:
        return 'Unknown Package'


# ==================================   Room  ==================================
@app.route('/add_room', methods=['POST'])
def add_room():
    """
    uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    type = fields.Int(required=True)
    apartment_uuid = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'room_id': id}
    """
    if check_auth_header_secret():
        return add_new_room()
    else:
        return 'Unknown Package'


@app.route('/get_room', methods=['POST', 'GET'])
def get_room():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'roomData': room_dict}
    """
    if check_auth_header_secret():
        return get_room_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_room', methods=['PUT'])
def update_room():
    """
    uuid = fields.Str(required=True)
    room_uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    type = fields.Int(required=True)
    apartment_uuid = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'roomData': room_dict}
    """
    if check_auth_header_secret():
        return update_room_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_room', methods=['DELETE'])
def delete_room():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'room_id': id}
    """
    if check_auth_header_secret():
        return delete_room_by_id()
    else:
        return 'Unknown Package'


# ==================================   Questionnaire  =========================
@app.route('/add_questionnaire', methods=['POST'])
def add_questionnaire():
    """
    uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    room_uuid = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'questionnaire_id': id}
    """
    if check_auth_header_secret():
        return add_new_questionnaire()
    else:
        return 'Unknown Package'


@app.route('/get_questionnaire', methods=['GET', 'POST'])
def get_questionnaire():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'questionnaireData': questionnaire_dict}
    """
    if check_auth_header_secret():
        return get_questionnaire_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_questionnaire', methods=['PUT'])
def update_questionnaire():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    room_id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'questionnaireData': questionnaire_dict}
    """
    if check_auth_header_secret():
        return update_questionnaire_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_questionnaire', methods=['DELETE'])
def delete_questionnaire():
    """
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    :return: {'result_code': 0, 'error_message': '', 'questionnaire_id': id}
    """
    if check_auth_header_secret():
        return delete_questionnaire_by_id()
    else:
        return 'Unknown Package'


# ==================================   Item  ==================================
@app.route('/add_item', methods=['POST'])
def add_item():
    """
    uuid = fields.Str(required=True)
    type = fields.Int(required=True)
    name = fields.Str(required=True)
    questionnaire_uuid = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'item_uuid': id}
    """
    if check_auth_header_secret():
        return add_new_item()
    else:
        return 'Unknown Package'


@app.route('/get_item', methods=['POST', 'GET'])
def get_item():
    """
    uuid = fields.Str(required=True)
    item_uuid = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'itemData': item_dict}
    """
    if check_auth_header_secret():
        return get_item_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_item', methods=['PUT'])
def update_item():
    """
    uuid = fields.Str(required=True)
    item_uuid = fields.Str(required=True)
    type = fields.Int(required=True)
    name = fields.Str(required=True)
    questionnaire_uuid = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'itemData': item_dict}
    """
    if check_auth_header_secret():
        return update_item_by_uuid()
    else:
        return 'Unknown Package'


@app.route('/delete_item', methods=['DELETE'])
def delete_item():
    """
    uuid = fields.Str(required=True)
    item_uuid = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'item_id': id}
    """
    if check_auth_header_secret():
        return delete_item_by_id()
    else:
        return 'Unknown Package'


# ==================================   Question  ==============================
@app.route('/add_question', methods=['POST'])
def add_question():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    type = fields.Int(required=True)
    text = fields.Str(required=True)
    questionnaire_id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'question_id': id}
    """
    if check_auth_header_secret():
        return add_new_question()
    else:
        return 'Unknown Package'


@app.route('/get_question', methods=['POST', 'GET'])
def get_question():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'questionData': question_dict}
    """
    if check_auth_header_secret():
        return get_question_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_question', methods=['PUT'])
def update_question():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    type = fields.Int(required=True)
    text = fields.Str(required=True)
    questionnaire_id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'questionData': question_dict}
    """
    if check_auth_header_secret():
        return update_question_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_question', methods=['DELETE'])
def delete_question():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'question_id': id}
    """
    if check_auth_header_secret():
        return delete_question_by_id()
    else:
        return 'Unknown Package'


# ==================================   Answer  ================================
@app.route('/add_answer', methods=['POST'])
def add_answer():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    text = fields.Str(required=True)
    question_id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'answer_id': id}
    """
    if check_auth_header_secret():
        return add_new_answer()
    else:
        return 'Unknown Package'


@app.route('/get_answer', methods=['GET', 'POST'])
def get_answer():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'answerData': answer_dict}
    """
    if check_auth_header_secret():
        return get_answer_by_id()
    else:
        return 'Unknown Package'


@app.route('/update_answer', methods=['PUT'])
def update_answer():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    text = fields.Str(required=True)
    question_id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'answerData': answer_dict}
    """
    if check_auth_header_secret():
        return update_answer_by_id()
    else:
        return 'Unknown Package'


@app.route('/delete_answer', methods=['DELETE'])
def delete_answer():
    """
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'answer_id': id}
    """
    if check_auth_header_secret():
        return delete_answer_by_id()
    else:
        return 'Unknown Package'


# ==================================   Suppliers  =============================
# TODO
# Holds, Name, type, contact person and so...  TODO
# TODO


# ==================================   Customer Feedback  =====================


# ==================================   Analytics  =============================
@app.route('/add_analytics', methods=['POST'])
def add_analytics():
    """
    uuid = fields.Str(required=True)
    event = fields.Int(required=True)
    data = fields.Str(required=True)
    :return: {'result_code': 0, 'error_message': '', 'analitcs_id': id}
    """
    if check_auth_header_secret():
        return add_new_analytics()
    else:
        return 'Unknown Package'


# ==================================   General  ===============================
def check_auth_header_secret():
    """
    Check if the incoming request's header contains our secretr key
    :return: true if it contains
    """
    bearer_header = request.headers.get('Authorization')
    return app.config.get('SECRET_KEY') == bearer_header

# You need to call app.run last, as it blocks execution of anything after it until the server is killed.
# Preferably, use the flask run command instead.
# Ref: https://github.com/pallets/flask/issues/2415
# app.run(debug=True, use_debugger=True, use_reloader=False, passthrough_errors=True)

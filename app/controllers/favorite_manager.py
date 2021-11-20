import json
from flask import jsonify

from app import db
from app.config.constants import ErrorCodes
from app.utils.exception_util import create_error_response
from app.utils.schema_utils import validate_schema
from datetime import datetime
from app.utils.uuid_utils import generate_uuid

from app.controllers.user_manager import is_user_login
from app.models import User, Favorite
from app.controllers.schemas import AddNewFavoriteSchema, GetAllFavoriteScheme, GetFavoriteByIdScheme, \
    UpdateFavoriteByIdScheme, DeleteFavoriteByIdScheme

add_new_favorite_schema = AddNewFavoriteSchema()
get_all_favorite_scheme = GetAllFavoriteScheme()
get_favorite_by_id_scheme = GetFavoriteByIdScheme()
update_favorite_by_id_scheme = UpdateFavoriteByIdScheme()
delete_favorite_by_id_scheme = DeleteFavoriteByIdScheme()


def generate_add_favorite_success_response(id: int):
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'favorite_uuid': id})


def generate_get_favorite_response(favorite: dict) -> json:
    return jsonify({'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value, 'error_message': '', 'favorite': favorite})


def generate_get_favorites_response(favorites_list: []) -> json:
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
         'error_message': '',
         'favorites': favorites_list})


def generate_favorite_deleted_successfuly(id: int) -> json:
    return jsonify(
        {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
         'error_message': '',
         'favorite_id': id})


def generate_favorite_not_found_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_FAVORITE_NOT_FOUND, 'favorite not found'))


def generate_user_not_found_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_FOUND, 'User not found'))


def generate_user_not_login_response() -> json:
    return jsonify(create_error_response(ErrorCodes.ERROR_CODE_USER_NOT_LOGGED_IN, 'User not logged in'))


@validate_schema(add_new_favorite_schema)
def add_new_favorite(data):
    uuid = data.get('uuid')
    name = data.get('name')
    item_uuid = data.get('item_uuid')
    item_type = data.get('item_type')
    username = is_user_login(uuid)
    if username:
        user = db.session.query(User).filter_by(username=username).first()
        if user:
            user_id = user.id
            favorite = Favorite(owner_id=user_id, name=name, item_uuid=item_uuid, item_type=item_type)
            favorite.save()
            return generate_add_favorite_success_response(favorite.id)
        else:
            return generate_user_not_found_response()
    else:
        return generate_user_not_login_response()


@validate_schema(get_all_favorite_scheme)
def get_all_favorites(data):
    uuid = data.get('uuid')
    username = is_user_login(uuid)
    if username:
        user = db.session.query(User).filter_by(username=username).first()
        if user:
            favorites_list = []
            favorites = db.session.query(Favorite).filter_by(owner_id=user.id).all()
            for favorite in favorites:
                favorites_list.append(favorite.to_dict())
            return generate_get_favorites_response(favorites_list)
        else:
            return generate_user_not_found_response()
    else:
        return generate_user_not_login_response()


@validate_schema(get_favorite_by_id_scheme)
def get_favorite_by_id(data):
    uuid = data.get('uuid')
    favorite_id: int = data.get('id')
    username = is_user_login(uuid)
    if username:
        user = db.session.query(User).filter_by(username=username).first()
        if user:
            favorite = db.session.query(Favorite).get(favorite_id)
            if favorite:
                return generate_get_favorite_response(favorite.to_dict())
            else:
                return generate_favorite_not_found_response()
        else:
            return generate_user_not_found_response()
    else:
        return generate_user_not_login_response()


@validate_schema(update_favorite_by_id_scheme)
def update_favorite_by_id(data):
    uuid = data.get('uuid')
    favorite_id: int = data.get('id')
    name = data.get('name')
    item_uuid = data.get('item_uuid')
    item_type = data.get('item_type')
    username = is_user_login(uuid)
    if username:
        user = db.session.query(User).filter_by(username=username).first()
        if user:
            favorite = db.session.query(Favorite).get(favorite_id)
            if favorite:
                favorite.name = name
                favorite.item_uuid = item_uuid
                favorite.item_type = item_type
                favorite.update_favorite()
                favorite_dict = favorite.to_dict()
                return jsonify(
                    {'result_code': ErrorCodes.ERROR_CODE_SUCCESS.value,
                     'error_message': '',
                     'vavorite': favorite_dict})
            else:
                return generate_favorite_not_found_response()
        else:
            return generate_user_not_found_response()
    else:
        return generate_user_not_login_response()

@validate_schema(delete_favorite_by_id_scheme)
def delete_favorite_by_id(data):
    uuid = data.get('uuid')
    favorite_id: int = data.get('id')
    username = is_user_login(uuid)
    if username:
        user = db.session.query(User).filter_by(username=username).first()
        if user:
            favorite = db.session.query(Favorite).get(favorite_id)
            if favorite and favorite.owner_id == user.id:
                favorite.delete_favorite()
                return generate_favorite_deleted_successfuly(favorite_id)
            else:
                return generate_favorite_not_found_response()
        else:
            return generate_user_not_found_response()
    else:
        return generate_user_not_login_response()

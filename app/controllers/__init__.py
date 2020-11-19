from app.controllers.user_manager import admin_user_register, is_admim_exist
from app.config.user_status import UserStatus
from app import db

if is_admim_exist() is True:
    print('Admin User already added')
else:
    db.create_all()
    user_data = {
        'username': 'AdminApp',
        'password': 'AdminApp2020!@',
        'language': 'eng',
        'status': UserStatus.ADMIN_USER.value
    }
    admin_user_register(data=user_data)
    print('Admin user added to database')
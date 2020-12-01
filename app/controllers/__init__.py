from app.controllers.user_manager import admin_user_register, is_admin_exist
from app.config.user_status import UserStatus
from app import db

if is_admin_exist() is True:
    print('Admin User already added')
else:
    db.create_all()
    user_data = {
        'username': 'AdminApp',
        'password': 'AdminApp2020!@',
        'language': 'eng',
        'status': UserStatus.ADMIN_USER.value,
        'phone': '+972522405134',
        'email': 'eyal@em-projects.com',
        'company_id': 1000000000,
    }
    admin_user_register(data=user_data)
    print('Admin user added to database')
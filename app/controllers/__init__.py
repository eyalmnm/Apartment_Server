from app.controllers.user_manager import admin_user_register, is_admin_exist
from app.controllers.company_manager import insert_new_company, is_company_exist
from app.config.user_status import UserStatus
from app.config.secrets import admin, companies
from app import db
import threading

if is_admin_exist() is True:
    print('Admin User already added')
else:
    db.create_all()
    user_data = {
        'username': admin.get('username'),
        'password': admin.get('password'),
        'language': 'eng',
        'status': UserStatus.SUPER_ADMIN_USER.value,
        'phone': '+972522405134',
        'email': 'eyal@em-projects.com',
        'company_id': '1000000000',
    }
    try:
        admin_user_register(data=user_data)
        print('Admin user added to database')
    except Exception as ex:
        print(ex)


def init_companies(data):
    for company in companies:
        try:
            print(f'Company: {company}')
            if is_company_exist(company.get('uuid')):
                print(f'{company.get("name")} already exist')
                continue
            insert_new_company(company)
            print(f'Company {company.get("name")} added to database {data}')
        except Exception as ex:
            print(ex)


x = threading.Thread(target=init_companies, args=(0,))
print('start add companies')
x.start()
print('companies added')

# def init_companies(data):
#     try:
#         company = companies[0]
#         print(f'Company: {company}')
#         insert_new_company(company)
#         print(f'Company {company.name} added to database {data}')
#     except Exception as ex:
#         print(ex)

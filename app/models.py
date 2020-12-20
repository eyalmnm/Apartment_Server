from datetime import timedelta, datetime

import jwt
from sqlalchemy.orm import relationship, backref

from app import db, app
from app.utils.uuid_utils import check_hash_password


# Ref: https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way-part-2#toc-automate-tests
# Ref: https://stackoverflow.com/a/2454618    //  To Dict
# Ref: https://pyjwt.readthedocs.io/en/stable/  // JWT Library

# For Company and Questionnaire
# Ref: https://stackoverflow.com/questions/34802851/foreign-key-to-same-table-in-sqlalchemy
# Ref: https://stackoverflow.com/questions/8872451/sqlalchemy-multiple-foreign-keys-to-same-table-with-compound-primary-key
# Ref: https://stackoverflow.com/questions/16976967/sqlalchemy-multiple-foreign-keys-to-same-table
# Ref: https://stackoverflow.com/questions/54913197/foreign-keys-and-inheritance-in-sql-alchemy
# Ref: https://stackoverflow.com/questions/32898831/one-object-two-foreign-keys-to-the-same-table
# Ref: https://stackoverflow.com/questions/34775701/one-to-many-relationship-on-same-table-in-sqlalchemy

# ==================================   Session  ===============================
class Session(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True, nullable=False)
    uuid = db.Column(db.String(128), index=True, unique=True, nullable=False)

    def __init__(self, username: str, uuid: str):
        self.username = username
        self.uuid = uuid

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_session(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Session {}>'.format(self.username)


# ==================================   User  ==================================
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    phone = db.Column(db.String(128), index=True, unique=False, nullable=False)
    password_hash = db.Column(db.String(128))
    salt = db.Column(db.String(128))
    language = db.Column(db.String(32))
    status = db.Column(db.Integer, nullable=False)
    company_uuid = db.Column(db.String, db.ForeignKey('company.uuid'), nullable=True)  # ForeignKey Company table

    def __init__(self, username: str, email: str, phone: str, hash_pwd: str, salt: str, language: str, status: int,
                 company_uuid: str):
        self.username = username
        self.email = email
        self.phone = phone
        self.password_hash = hash_pwd
        self.salt = salt
        self.language = language
        self.status = status
        self.company_uuid = company_uuid

    def save_admin(self):
        db.session.add(self)
        db.session.commit()

    def save(self, session):
        db.session.add(self)
        db.session.add(session)
        db.session.commit()

    def save_with_session(self, session):
        db.session.add(self)
        db.session.add(session)
        db.session.commit()

    def update_user(self):
        db.session.commit()

    def delete_user(self):
        self.delete()
        db.session.commit()

    def password_is_valid(self, password):
        return check_hash_password(self.password_hash, self.salt, password)

    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def __repr__(self):
        return '<User {}>'.format(self.username)


# ==================================   Company  ===============================
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    registration_id = db.Column(db.String(128), index=True, nullable=False)
    address = db.Column(db.String(256), index=True, nullable=False)
    city = db.Column(db.String(256), index=True, nullable=False)
    state = db.Column(db.String(64), index=True, nullable=True)
    country = db.Column(db.String(64), index=True, nullable=False)
    zip_code = db.Column(db.String(64), index=True, nullable=False)
    phone = db.Column(db.String(64), index=True, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    uuid = db.Column(db.String(64), index=True, nullable=False)
    parent_company_id = db.Column(db.Integer(), db.ForeignKey('company.id'), nullable=True)

    # Child companies
    sub_companies = relationship("Company", backref=backref('parent', remote_side=[id]), lazy='dynamic')

    # rooms = db.relationship('Room', backref='floor', lazy='dynamic') Change This line
    # textures = db.relationship('FloorTexture', backref='floor', lazy='dynamic')  Change This line

    def __init__(self, name: str, registration_id: str, address: str, city: str, state: str, country: str,
                 zip_code: str,
                 phone: str, status: int, parent_company_id: str, uuid: str):
        self.name = name
        self.registration_id = registration_id
        self.parent_company_id = parent_company_id
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.zip_code = zip_code
        self.phone = phone
        self.status = status
        self.uuid = uuid

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_company(self):
        db.session.commit()

    def delete_company(self):
        self.delete()
        db.session.commit()

    def set_owner(self, owner_id):
        self.owner = owner_id
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        serialized["sub_companies"] = [company.to_dict() for company in self.sub_companies]
        # serialized["rooms"] = [room.to_dict() for room in self.rooms] Change This line
        # serialized["paintings"] = [painting.to_dict() for painting in self.paintings]  Change This line
        return serialized

    def __repr__(self):
        return '<Company {}>'.format(self.name)


# ==================================   Country  ===============================
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_country(self):
        db.session.commit()

    def delete_country(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        return serialized

    def __repr__(self):
        return '<Country {}>'.format(self.name)


# ==================================   State  =================================
class State(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    def __init__(self, name, country_id):
        self.name = name
        self.country_id = country_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_state(self):
        db.session.commit()

    def delete_state(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        return serialized

    def __repr__(self):
        return '<State {}>'.format(self.name)


# ==================================   City  ==================================
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    def __init__(self, name, state_id):
        self.name = name
        self.state_id = state_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_city(self):
        db.session.commit()

    def delete_city(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        return serialized

    def __repr__(self):
        return '<City {}>'.format(self.name)


# ==================================   Street  ================================
class Street(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    def __init__(self, name, city_id):
        self.name = name
        self.city_id = city_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_street(self):
        db.session.commit()

    def delete_street(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        return serialized

    def __repr__(self):
        return '<Street {}>'.format(self.name)


# ==================================   Building  ==============================
class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(256), index=True, nullable=True)
    # street_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)

    entrances = relationship("Entrance", backref="building")
    # street = relationship("Street")

    def __init__(self, name, company_id, latitude, longitude, address):
        self.name = name
        self.company_id = company_id
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        # def __init__(self, name, street_id, company_id):
        # self.street_id = street_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_building(self):
        db.session.commit()

    def delete_building(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        serialized["entrances"] = [entrance.to_dict() for entrance in self.entrances]
        # serialized["street"] = self.street.to_dict() if self.street else None
        return serialized

    def __repr__(self):
        return '<Building {}>'.format(self.name)


# ==================================   Entrance  ==============================
class Entrance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'), nullable=False)

    floors = relationship("Floor", backref="entrance")

    def __init__(self, name, building_id):
        self.name = name
        self.building_id = building_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_entrance(self):
        db.session.commit()

    def delete_entrance(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        serialized["floors"] = [floor.to_dict() for floor in self.floors]
        return serialized

    def __repr__(self):
        return '<Entrance {}>'.format(self.name)


# ==================================   Floor  =================================
class Floor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    entrance_id = db.Column(db.Integer, db.ForeignKey('entrance.id'), nullable=False)

    apartments = relationship("Apartment", backref="floor")

    def __init__(self, name, entrance_id):
        self.name = name
        self.entrance_id = entrance_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_floor(self):
        db.session.commit()

    def delete_floor(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        serialized["apartments"] = [apartment.to_dict() for apartment in self.apartments]
        return serialized

    def __repr__(self):
        return '<Floor {}>'.format(self.name)


# ==================================   Apartment  =============================
class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    rooms = relationship("Room", backref="apartment")

    def __init__(self, name, floor_id, company_id):
        self.name = name
        self.floor_id = floor_id
        self.company_id = company_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_apartment(self):
        db.session.commit()

    def delete_apartment(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        serialized["rooms"] = [room.to_dict() for room in self.rooms]
        return serialized

    def __repr__(self):
        return '<Apartment {}>'.format(self.name)


# ==================================   Room  ==================================
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    type = db.Column(db.Integer, index=False, nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)

    questionnaires = relationship("Questionnaire", backref="room")

    def __init__(self, name, apartment_id, type):
        self.name = name
        self.type = type
        self.apartment_id = apartment_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_room(self):
        db.session.commit()

    def delete_room(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        serialized["questionnaires"] = [questionnaire.to_dict() for questionnaire in self.questionnaires]
        return serialized

    def __repr__(self):
        return '<Apartment {}>'.format(self.name)


# ==================================   Questionnaire  =========================
class Questionnaire(db.Model):
    id = db.Column(db.String(128), primary_key=True, index=True, nullable=False)
    name = db.Column(db.String(128), index=True, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    parent_questionnaire = db.Column(db.String(128), db.ForeignKey("questionnaire.id"), nullable=False)

    questions = relationship("Question", backref="questionnaire")

    def __init__(self, id, name, room_id, parent_questionnaire):
        self.name = name
        self.room_id = room_id
        self.parent_questionnaire = parent_questionnaire

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_questionnaire(self):
        db.session.commit()

    def delete_questionnaire(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        serialized["questions"] = [question.to_dict() for question in self.questions]
        return serialized

    def __repr__(self):
        return '<Questionnaire {}>'.format(self.name)


# ==================================   Question  ==============================
class Question(db.Model):
    id = db.Column(db.String(128), primary_key=True, index=True, nullable=False)
    type = db.Column(db.Integer, index=True, nullable=False)
    text = db.Column(db.String(128), index=True, nullable=False)
    questionnaire_uuid = db.Column(db.String(128), db.ForeignKey('questionnaire.id'), nullable=False)
    # uuid = db.Column(db.String(128), index=True, nullable=False)

    answers = relationship("Answer", backref="question")

    def __init__(self, id, question_type, text, questionnaire_uuid):  # , uuid):
        self.id = id
        self.type = question_type
        self.text = text
        self.questionnaire_uuid = questionnaire_uuid
        # self.uuid = uuid

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_question(self):
        db.session.commit()

    def delete_question(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        serialized = dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))
        # serialized = self.device.to_dict() if self.device else None
        serialized["answers"] = [answer.to_dict() for answer in self.answers]
        return serialized

    def __repr__(self):
        return '<Question {}>'.format(self.name)


# ==================================   Answer  ================================
class Answer(db.Model):
    id = db.Column(db.String(128), index=True, nullable=False, primary_key=True)
    text = db.Column(db.String(2048), index=True, nullable=False)  # in case of outbound - hint
    question_uuid = db.Column(db.String(128), db.ForeignKey('question.id'), nullable=False)

    def __init__(self, text, question_uuid, id):
        self.text = text
        self.question_uuid = question_uuid
        self.id = id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_answer(self):
        db.session.commit()

    def delete_answer(self):
        self.delete()
        db.session.commit()

    def to_dict(self):
        return dict((col, getattr(self, col)) for col in list(self.__table__.columns.keys()))

    def __repr__(self):
        return '<answer {}>'.format(self.text)


# ==================================   Analytics  =============================
class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event = db.Column(db.Integer(), index=True, nullable=False)
    data = db.Column(db.String(2048), index=False, nullable=False)

    def __init__(self, event, data):
        self.event = event
        self.data = data

    def save(self):
        db.session.add(self)
        db.session.commit()

import uuid
import hashlib
from datetime import datetime
import jwt
from app import app


# Ref: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
# Ref: https://realpython.com/token-based-authentication-with-flask/


def get_salt():
    # return uuid.uuid4().bytes
    return uuid.uuid4().hex


def get_hash_password(salt, password):
    # return hashlib.sha512(password + salt).digest()
    return hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()


def check_hash_password(hash_pwd, salt, password):
    generated_hash = get_hash_password(salt=salt, password=password)
    if generated_hash == hash_pwd:
        return True
    else:
        return False


def generate_uuid():
    return uuid.uuid4().hex


# Ref: https://realpython.com/token-based-authentication-with-flask/
def encode_auth_token(self, user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

import os

# Ref: https://stackoverflow.com/questions/50846856/in-flask-sqlalchemy-how-do-i-set-check-same-thread-false-in-config-py

basedir = os.path.abspath(os.path.dirname(__file__))


class AppConfig(object):
    # The key is Sha-256 of Apartment_Evidence_Israel_Raanana_em-projects_2020_11_11
    # (https://emn178.github.io/online-tools/sha256.html)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cc1211b6e6813549aa05404c1d6c66f617646eeeeac92eaad72b653951ab0e26'

    # SQLite Configuration
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')) + \
                              '?check_same_thread=False '
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Current Configuration
    ENV = 'DEV'  # DEV or PRO
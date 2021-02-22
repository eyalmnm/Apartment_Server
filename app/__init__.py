from flask import Flask
from app_config import AppConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(AppConfig)
db: SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

# Model creation must come before table creation
# db.create_all()
# db.session.commit()
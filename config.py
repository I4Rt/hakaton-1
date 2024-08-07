from flask import Flask

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from flask_cors import CORS, cross_origin





app = Flask(__name__, template_folder='resources/templates', static_folder='resources/static', static_url_path = '')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost:5432/fire_detection_db'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


# app has been set and configured
Base = declarative_base()
e = create_engine("postgresql://postgres:qwerty@localhost:5432/fire_detection_db", echo=False)
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

myapp = Flask(__name__)

myapp.config.from_object(Config)

db = SQLAlchemy(myapp)
migrate = Migrate(myapp, db)

login = LoginManager(myapp)
login.login_view = 'login' # The 'login' value here is the function (or endpoint) name for the login view

from app import routes, models # forms.py is imported from within models.py 


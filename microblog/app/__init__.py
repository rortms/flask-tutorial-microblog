from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_babel import lazy_gettext as _l

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from flask import request # see language translation below

myapp = Flask(__name__)

#################
# Load config class
myapp.config.from_object(Config)


#################
# Load Database
db = SQLAlchemy(myapp)
migrate = Migrate(myapp, db)

#################
# Login Manager
login = LoginManager(myapp)
login.login_view = 'login' # The 'login' value here is the function (or endpoint) name for the login view
login.login_message = _l('Please log in to access this page.')

#################
# Email setup
mail = Mail(myapp)

#################
# Front-end frame work
bootstrap = Bootstrap(myapp)

#################
# Timezone managment
moment = Moment(myapp)

#################
# Translations
babel = Babel(myapp)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(myapp.config['LANGUAGES'])
    # return 'es' # testing, force display spanish translation
    
#####################
# Email bug reporting
if not myapp.debug:
    if myapp.config['MAIL_SERVER']:
        auth = None
        if myapp.config['MAIL_USERNAME'] or myapp.config['MAIL_PASSWORD']:
            auth = (myapp.config['MAIL_USERNAME'], myapp.config['MAIL_PASSWORD'])
        secure = None
        if myapp.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost = (myapp.config['MAIL_SERVER'], myapp.config['MAIL_PORT']),
            fromaddr='no-reply@' + myapp.config['MAIL_SERVER'],
            toaddrs=myapp.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        myapp.logger.addHandler(mail_handler)

        
#################
# Logging to File
if not myapp.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    myapp.logger.addHandler(file_handler)

    myapp.logger.setLevel(logging.INFO)
    myapp.logger.info('Microblog startup')
    

#
from app import routes, models, errors # forms.py is imported from within models.py 

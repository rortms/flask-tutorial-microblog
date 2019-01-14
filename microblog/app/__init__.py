from flask import Flask, request, current_app
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


###############################
# Application Factory Function
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    
    
    #################
    # Load Database
    db.init_app(app)
    migrate.init_app(app, db)


    #################
    # Login Manager
    login.init_app(app)

    #################
    # Email setup
    mail.init_app(app)


    #################
    # Front-end frame work
    bootstrap.init_app(app)


    #################
    # Timezone managment
    moment.init_app(app)


    #################
    # Translations
    babel.init_app(app)


    ########################
    # Blueprint Registration
    
    # Errors
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Auth
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Main
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    

    ##############
    # Logs/Reports
    if not app.debug and not app.testing:
        
        #####################
        # Email bug reporting
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    
        #################
        # Logging to File
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')
            
    ###
    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    # return 'es' # testing, force display spanish translation


#
from app import models  

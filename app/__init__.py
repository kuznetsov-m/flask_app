import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from elasticsearch import Elasticsearch
import certifi

from redis import Redis
import rq

from config import BaseConfig

db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()
# Если пользователь, который не выполнил вход в систему, пытается просмотреть защищенную страницу, Flask-Login автоматически перенаправляет пользователя в форму для входа и только после завершения процесса входа в систем перенаправляет на страницу, которую пользователь хотел просмотреть.
# Flask-Login должен знать, что такое функция просмотра, которая обрабатывает логины.
# Значение «login» выше является именем функции (или конечной точки) для входа в систему.
login.login_view = 'auth.login'

bootstrap = Bootstrap()
moment = Moment()

def create_app(config_class=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if app.config['ELASTICSEARCH_URL']:
        app.elasticsearch = Elasticsearch(
            [app.config['ELASTICSEARCH_URL']],
            # use_ssl=False,
            # ca_certs=certifi.where()
        )
    else:
        app.elasticsearch = None
    
    # redis
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('flask_app-tasks', connection=app.redis)

    if not app.debug and not app.testing:
        # Logs
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            # Log file
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes=10240,
                                            backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('flask_app startup')


        # Log mail server
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='flask_app Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app

from app import models
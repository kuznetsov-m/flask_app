import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8bp\x0c...'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    if 'postgres' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail server
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['email@gmail.com']

    # other
    POSTS_PER_PAGE = 25

    # elasticsearch
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    # heroku
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # redis
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

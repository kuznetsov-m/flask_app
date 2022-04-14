import os

# default config
class BaseConfig(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8bp\x0c...'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

import os


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(os.path.abspath(os.path.dirname(__file__)), '../Paprica/paprica.db')
    UPLOAD_DIR = os.path.curdir = 'static/uploads/'
    SECRET_KEY = os.getenv('SECRET_KEY')

class ProductionConfig(Config):
    DEBUG = True
    pass

class DevelopmentConfig(Config):
    pass

import os
import secret
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.environ.get('SECRET_KEY') or secret.CONF_SECRET_KEY
    SECRET_KEY = os.urandom(32)
    WTF_CSRF_SECRET_KEY = "a csrf secret key"

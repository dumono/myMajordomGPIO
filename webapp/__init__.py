# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'
login.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."

bootstrap = Bootstrap(app)

from webapp import routes, models

if not models.User.query.first():
    default_user = models.User(email='admin@exampl.com', username='admin', password_hash=generate_password_hash('admin', method='sha256'))

    db.session.add(default_user)
    db.session.commit()
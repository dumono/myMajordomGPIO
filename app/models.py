from app import db, login

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class GPIO_connect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    GPIO_NUM= db.Column(db.Integer, unique=True)
    comment = db.Column(db.String(120))

class GlobalConf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(128), index=True, unique=True)
    val = db.Column(db.String(128))
    comment = db.Column(db.String(128))

    def __repr__(self):
        return f'{self.key} {self.val} {self.comment}'

class GPIO_Types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gpioType = db.Column(db.String(16), index=True, unique=True)
from webapp import db, login

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


class GPIO_connect(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
    gpio_type = db.Column(db.String(64))
    gpio_num = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.String(64))
#    comment = db.Column(db.String(120))


class GlobalConf(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(128), index=True, primary_key=True)
    val = db.Column(db.String(128))
    comment = db.Column(db.String(128))

    def __repr__(self):
        return f'{self.key} {self.val} {self.comment}'

class GPIOTypes(db.Model):
    gpioType = db.Column(db.String(16), index=True, primary_key=True)

    def __repr__(self):
        return self.gpioType

class GpioRules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signal_pin = db.Column(db.Integer)
    signal_type = db.Column(db.String(16))
    condition = db.Column(db.String(3))
    condition_value = db.Column(db.String(10))
    action_type = db.Column(db.String(10))
    action_pin = db.Column(db.Integer)
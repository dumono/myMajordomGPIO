from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SettingsForm(FlaskForm):
    key = StringField('Ключ', validators=[DataRequired()])
    value = StringField('Значение', validators=[DataRequired()])
    comment = StringField('Описание', validators=[DataRequired()])
    submit = SubmitField('Добавить')

class GPIOTypesForm(FlaskForm):
    value = StringField('Тип', validators=[DataRequired()])
    submit = SubmitField('Добавить')

class GPIOEdit(FlaskForm):
    value = StringField('Тип', validators=[DataRequired()])

    submit = SubmitField('Добавить')
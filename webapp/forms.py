from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
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

class GPIORulesForm(FlaskForm):
    signal_pin = IntegerField('SygnalPin', validators=[DataRequired()])
    signal_type = SelectField('Тип устройства', choices=[('DHT11', 'DHT11'), ('switch', 'Выключатель')], validate_choice=True)
    condition = SelectField('Тип условия', choices=[('min', '<'), ('max', '>'), ('eq', '=')], validate_choice=True)
    condition_value = StringField('Условие', validators=[DataRequired()])
    action_type = SelectField('Тип действия', choices=[('on', 'ВКЛ'), ('off', 'Выкл')], validate_choice=True)
    action_pin = IntegerField('ActionPin', validators=[DataRequired()])
    submit = SubmitField('Добавить')
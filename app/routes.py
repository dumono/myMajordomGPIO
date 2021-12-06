from app import app, db

from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, SettingsForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, GlobalConf
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if request.method == 'POST':
    #if form.validate_on_submit():
        conf = GlobalConf(key=form.key.data, val=form.value.data, comment=form.comment.data)
        db.session.add(conf)
        db.session.commit()
        flash('Значение добавлено')
        return redirect(url_for('settings'))
    else:
        config =db.session.query(GlobalConf).all()
    return render_template('settings.html', title='Настройки', form=form, config=config)


@app.route('/gpio_types', methods=['GET', 'POST'])
@login_required
def gpio_types():
    pass

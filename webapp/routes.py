from webapp import app, db

from flask import render_template, flash, redirect, url_for, request
from webapp.forms import LoginForm, SettingsForm, GPIOTypesForm, GPIORulesForm
from flask_login import current_user, login_user, logout_user, login_required
from webapp.models import User, GlobalConf, GPIOTypes, GPIO_connect, GpioRules
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    gpc = []
    gpc1 = db.session.query(GPIO_connect.gpio_type).all()
    for i in gpc1:
        for j in i:
            gpc.append(j)
    return render_template('index.html', title='Home', gpc=gpc)

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
        config = db.session.query(GlobalConf).all()
    return render_template('settings.html', title='Настройки', form=form, config=config)

@login_required
@app.route("/update", methods=["POST"])
def update():
    updatekey = request.form.get("updatedkey")
    updatedval = request.form.get("updatedval")
    updatedcomm = request.form.get("updatedcomm")
    conf = GlobalConf.query.filter_by(key=updatekey).first()
    conf.val = updatedval
    conf.comment = updatedcomm
    db.session.commit()
    return redirect("/settings")

@app.route('/edit_gpio_types', methods=['GET', 'POST'])
@login_required
def edit_gpio_types():
    form = GPIOTypesForm()
    if request.method == 'POST':
        gpio_TP = GPIOTypes(gpioType=form.value.data)
        db.session.add(gpio_TP)
        db.session.commit()
        flash('Значение добавлено')
        return redirect(url_for('edit_gpio_types'))
    else:
        gpio_TP = db.session.query(GPIOTypes).all()
    return render_template("edit_gpio_types.html", gpio_TP=gpio_TP, form=form )


@login_required
@app.route("/gpio_uptd", methods=["POST"])
def gpio_uptd():
    gpio_type = request.form.get("gpio_type")
    gpio_num = request.form.get("gpio_num")
#    print(gpio_type, gpio_num)
    conf = GPIO_connect.query.filter_by(gpio_num=gpio_num).first()
    conf.gpio_type = gpio_type
    conf.gpio_num = gpio_num
    db.session.commit()
    return redirect("/edit_gpio")

@app.route('/edit_gpio', methods=['GET','POST'])
@login_required
def edit_gpio():
    # если не использовать такие циклы, то получается несовпадение данных
    # gpio_TP: [GND, GPIO, +5V, +3V]
    # gpc: ['+5V', ' 2 ', 'GND', 'GND', 'GND'....
    gpio_TP = []
    gpc = []
    gpio_TP_all = db.session.query(GPIOTypes).all()
    for i in gpio_TP_all:
        gpio_TP.append(str(i))
    gpc1 = db.session.query(GPIO_connect.gpio_type).all()
#    print(gpc1)
    for i in gpc1:
        for j in i:
            gpc.append(j)
#    print(gpc)
#    print(gpio_TP)
    return render_template('edit_GPIO.html', gpio_TP=gpio_TP, gpc=gpc)

@app.route('/edit_gpio_rules', methods=['GET','POST'])
@login_required
def edit_gpio_rules():
    rules = db.session.query(GpioRules).all()
    form = GPIORulesForm()
    if request.method == 'POST':
        rule = GpioRules(signal_pin=form.signal_pin.data, signal_type=form.signal_type.data,
                         condition=form.condition.data, condition_value=form.condition_value.data,
                         action_type=form.action_type.data, action_pin=form.action_pin.data)
        db.session.add(rule)
        db.session.commit()
        flash('Значение добавлено')
        return redirect(url_for('edit_gpio_rules'))
    return render_template('edit_rules.html', rules=rules, form=form)


@app.route("/delete_rule", methods=["POST"])
@login_required
def delete_rule():
    rule_id = request.form.get("deletekey")
    db.session.query(GpioRules).filter(GpioRules.id == rule_id).delete()
    db.session.commit()
    flash('Правило удалено')
    return redirect(url_for('edit_gpio_rules'))
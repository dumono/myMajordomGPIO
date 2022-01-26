from celery import Celery
from celery.schedules import crontab
from webapp.models import GPIO_connect
from config import Config
from webapp import db

import platform


def verify_platform():
    if platform.node() == 'raspberrypi':
        return True
    return False


if verify_platform():
    import Adafruit_DHT

# flask_app = app
redis_addr = Config.REDIS_SERVER
celery_app = Celery('tasks', broker='redis://' + redis_addr + ':6379/0')


def get_pin_value(pin, type):
    if verify_platform():
        pass
    else:
        return 1


@celery_app.task
def update_gpio_values():
    gpc = []
    print('start')
    gpcn = db.session.query(GPIO_connect.gpio_num).all()
    for i in gpcn:
        print('i=', i)
        for j in i:
            print('j=', j)
            gpc_upd = GPIO_connect.query.filter_by(gpio_num=j).first()
            print('gpc_upd=', gpc_upd)
            gpc_upd.val = get_pin_value(j, gpc_upd.gpio_type)
            print(j, gpc_upd.gpio_type)
            db.session.commit()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), update_gpio_values.s())

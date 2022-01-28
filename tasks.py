from celery import Celery
from celery.schedules import crontab
from webapp.models import GPIO_connect, GpioRules
from config import Config
from webapp import db
#import RPi.GPIO as GPIO
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


def config_pin(pin, pin_type):
    if pin_type == 'GPIO_IN':
        GPIO.setup(pin, GPIO.IN)
    elif pin_type == 'GPIO_IN':
        GPIO.setup(pin, GPIO.OUT)

def get_pin_value(pin, pin_type, rec = False):
    if verify_platform():
        if pin_type == 'DHT11':
            humidity, temperature = Adafruit_DHT.read_retry(11, pin)
            if temperature is not None:
                return temperature
            else:
                return 'ERR'
        elif pin_type == 'GPIO_IN':
            try:
                if GPIO.input(pin) == GPIO.HIGH:
                    return 1
                else:
                    return 0
            except RuntimeError:
                if rec:
                    return 'NoCNF'
                else:
                    config_pin(pin, pin_type)
                    get_pin_value(pin, pin_type, True)
        elif pin_type == 'GPIO_OUT':
            try:
                if GPIO.output(pin) == GPIO.HIGH:
                    return 1
                else:
                    return 0
            except RuntimeError:
                if rec:
                    return 'NoCNF'
                else:
                    config_pin(pin, pin_type)
                    get_pin_value(pin, pin_type, True)
    else:
        return 'NoCNF'


@celery_app.task
def update_gpio_values():
    gpc = []
    #    print('start')
    gpcn = db.session.query(GPIO_connect.gpio_num).all()
    for i in gpcn:
#        print('i=', i)
        for j in i:
#            print('j=', j)
            gpc_upd = GPIO_connect.query.filter_by(gpio_num=j).first()
#            print('gpc_upd=', gpc_upd)
            gpc_upd.val = get_pin_value(j, gpc_upd.gpio_type)
#            print(j, gpc_upd.gpio_type)
            db.session.commit()

@celery_app.task
def check_rules():
    rules = db.session.query(GpioRules).all()
    # print(rules)
    for rule in rules:
        signal_pin = rule.signal_pin
        signal_type = rule.signal_type
        condition = rule.condition
        condition_value = rule.condition_value
        action_type = rule.action_type
        action_pin = rule.action_pin
        signal_pin_value = get_pin_value(signal_pin, signal_type)
        if condition == 'min':
            if signal_pin_value < condition_value:
                pass
        elif condition == 'max':
            if signal_pin_value > condition_value:
                pass
        elif condition == 'eq':
            if signal_pin_value == condition_value:
                pass


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(crontab(minute='*/1'), update_gpio_values.s())
    sender.add_periodic_task(10, update_gpio_values.s(), )

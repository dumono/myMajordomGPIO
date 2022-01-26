DEFAULT_PIN_NAME = "DFP"
DEFAULT_PIN_DESC = "DESC"
DEFAULT_PIN_TYPE = "GND"

class GPIO:
    pins = {}
    def __init__(self, count):
        for i in range(count):
            self.pins[i+1] = {'pin': DEFAULT_PIN_NAME, 'desc': DEFAULT_PIN_DESC, 'type': DEFAULT_PIN_TYPE }

    def get_pin_name(self, pin):
        return self.pins[pin]['pin']

    def set_pin_name(self, pin, value):
        self.pins[pin] = {'pin': value, 'desc': self.pins[pin]['desc']}

    def get_pin_desc(self, pin):
        return self.pins[pin]['desc']

    def set_pin_desc(self, pin, value):
        self.pins[pin] = {'pin': self.pins[pin]['pin'], 'desc': value}

    def get_pin_type(self, pin):
        return self.pins[pin]['desc']

    def set_pin_type(self, pin, value):
        self.pins[pin] = {'pin': self.pins[pin]['pin'], 'desc': value}
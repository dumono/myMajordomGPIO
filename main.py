'''from flask import Flask

webapp = Flask(__name__)


@webapp.route('/')
def hello_world():
    return 'Hello World'
'''

from webapp import app

if __name__ == '__main__':
    app.run()

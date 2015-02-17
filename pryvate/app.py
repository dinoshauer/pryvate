import os

from flask import Flask

from blueprints.simple import simple
from blueprints.pypi import pypi

app = Flask(__name__)
app.config['BASEDIR'] = './eggs/'

if not os.path.isdir(app.config['BASEDIR']):
    os.mkdir(app.config['BASEDIR'])

app.register_blueprint(simple)
app.register_blueprint(pypi)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

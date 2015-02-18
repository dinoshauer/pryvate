import os

from flask import Flask

from blueprints.packages import packages
from blueprints.pypi import pypi
from blueprints.simple import simple

app = Flask(__name__)
app.config['BASEDIR'] = './eggs/'
app.config['PYPI'] = 'https://pypi.python.org{}'

if not os.path.isdir(app.config['BASEDIR']):
    os.mkdir(app.config['BASEDIR'])

app.register_blueprint(packages.blueprint)
app.register_blueprint(pypi.blueprint)
app.register_blueprint(simple.blueprint)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

import os

from flask import Flask

from blueprints.pypi import pypi
from blueprints.simple import simple

app = Flask(__name__)
app.config['BASEDIR'] = './eggs/'

if not os.path.isdir(app.config['BASEDIR']):
    os.mkdir(app.config['BASEDIR'])

app.register_blueprint(simple.blueprint)
app.register_blueprint(pypi.blueprint)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

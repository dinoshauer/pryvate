"""Private PyPi repository and proxy."""
import os

from flask import Flask

from pryvate.blueprints.packages import packages
from pryvate.blueprints.pypi import pypi
from pryvate.blueprints.simple import simple

app = Flask(__name__)
app.config['BASEDIR'] = './eggs/'
app.config['PYPI'] = 'https://pypi.python.org{}'
app.config['PRIVATE_EGGS'] = {}

if not os.path.isdir(app.config['BASEDIR']):
    os.mkdir(app.config['BASEDIR'])

app.register_blueprint(packages.blueprint)
app.register_blueprint(pypi.blueprint)
app.register_blueprint(simple.blueprint)


def run(host=None, debug=False):
    """Start the server."""
    app.run(host=host, debug=debug)


if __name__ == '__main__':
    run(host='0.0.0.0', debug=True)

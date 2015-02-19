"""Private PyPi repository and proxy."""
import os

from flask import Flask

from pryvate.blueprints.packages import packages
from pryvate.blueprints.pypi import pypi
from pryvate.blueprints.simple import simple
from pryvate.defaultconfig import DefaultConfig

app = Flask(__name__)
app.config.from_object(DefaultConfig)
app.config.from_envvar('PRYVATE_CONFIG')

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

"""Private PyPi repository and proxy.

This is the main entrypoint for running the pryvate server.
It can be started in couple of different ways:

1. Importing it in a ``wsgi`` file, for a minimal setup all you need is::

    from pryvate.server import app

2. You can start it via the console script exposed from the installation::

    $ pryvate-server
"""
import os

from flask import Flask

from pryvate.blueprints.packages import packages
from pryvate.blueprints.pypi import pypi
from pryvate.blueprints.simple import simple
from pryvate.defaultconfig import DefaultConfig

app = Flask(__name__)
app.config.from_object(DefaultConfig)
if os.environ.get('PRYVATE_CONFIG'):
    app.config.from_envvar('PRYVATE_CONFIG')
else:
    app.logger.warning('env var PRYVATE_CONFIG not set, running with defaults')

if not os.path.isdir(app.config['BASEDIR']):
    os.mkdir(app.config['BASEDIR'])

app.register_blueprint(packages.blueprint)
app.register_blueprint(pypi.blueprint)
app.register_blueprint(simple.blueprint)


def run(host=None, debug=False):
    """Start the server.

    This function is only available for
    the console script exposed by installing
    the pryvate package.

    Keyword Arguments:
        host (``str``, optional): The interface the server will bind to
            *Default:* ``None``
        debug (``bool``, optional): Start the Flask server in debug mode
            *Default:* ``False``
    """
    app.run(host=host, debug=debug)


if __name__ == '__main__':
    run(host='0.0.0.0', debug=True)

"""Pryvate server."""
import os

from flask import Flask, g
from flask.ext import restful

from pryvate import api
from pryvate.blueprints.packages import packages
from pryvate.blueprints.pypi import pypi
from pryvate.blueprints.simple import simple
from pryvate.defaultconfig import DefaultConfig
from pryvate.db import PryvateSQLite

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

restful = restful.Api(app)
restful.add_resource(api.PackageList, '/api/packages')


@app.before_request
def before_request():
    """Start a database connection."""
    g.database = PryvateSQLite(app.config['DB_PATH'])


@app.teardown_request
def teardown_request(_):
    """Close the database connection if it exists."""
    database = getattr(g, 'database', None)
    if database is not None:
        database.connection.close()


def run():
    """Start the server.

    This function is only available for
    the console script exposed by installing
    the pryvate package.

    Note:
        This should only be used for debugging.
    """
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    run()

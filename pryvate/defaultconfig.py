"""Default Pryvate config."""


class DefaultConfig(object):

    """Class containing the default config for the Pryvate package.

    Anything can be overwritten! This is a regular old Flask configuration,
    read more here: http://flask.pocoo.org/docs/0.10/config/ and here
    http://flask.pocoo.org/docs/0.10/api/#flask.Flask.default_config

    The few options pryvate needs are:

    * ``BASEDIR`` - Where to store packages
    * ``PYPI`` - The url to the cheeseshop where public packages are stored
    * ``DB_PATH`` - Path or URI to a SQLite database (can be :memory:)
    * ``DB_URI`` - Set to ``True`` if using a URI for ``DB_PATH``
    """

    BASEDIR = './eggs/'
    PYPI = 'https://pypi.python.org{}'
    PRIVATE_EGGS = {}
    DB_PATH = '.pryvate.db'
    DB_URI = False

"""Simple blueprint."""
from flask import Blueprint

simple = Blueprint(
    'simple',
    __name__,
    url_prefix='/simple'
)


@simple.route('', methods=['GET'])
def get_simple():
    """Find a package and return the contents of it."""
    return 'ok'

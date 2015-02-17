"""PyPi blueprint."""
import os
from flask import Blueprint, current_app, request

pypi = Blueprint(
    'pypi',
    __name__,
    url_prefix='/pypi'
)


def register_package(request):
    package_dir = os.path.join(current_app.config['BASEDIR'],
                               request.form['name'].lower())
    if not os.path.isdir(package_dir):
        os.mkdir(package_dir)
    return 'ok'


def upload_package(request):
    pass


@pypi.route('', methods=['POST'])
def post_pypi():
    """Find a package and return the contents of it."""
    if not request.files:
        return register_package(request)
    else:
        return upload_package(request)

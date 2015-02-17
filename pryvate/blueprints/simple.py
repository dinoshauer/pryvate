"""Simple blueprint."""
import os

from flask import Blueprint, current_app

simple = Blueprint('simple', __name__, url_prefix='/simple',
                   template_folder='templates')


@simple.route('', methods=['GET'])
def get_simple():
    """List all packages."""
    packages = os.listdir(current_app.config['BASEDIR'])

    return 'ok'

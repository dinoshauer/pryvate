"""Package blueprint."""
import os

import magic
from flask import Blueprint, current_app, make_response, render_template

blueprint = Blueprint('packages', __name__, url_prefix='/packages')

@blueprint.route('')
def foo():
    return 'ok'

@blueprint.route('/<package_type>/<letter>/<name>/<version>',
                 methods=['GET', 'HEAD'])
def packages(package_type, letter, name, version):
    """Get the contents of a package."""
    filepath = os.path.join(current_app.config['BASEDIR'], name.lower(),
                            version.lower())
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as egg:
            mimetype = magic.from_file(filepath, mime=True)
            contents = egg.read()
            return make_response(contents, 200, {'Content-Type': mimetype})
    return make_response('Package not found', 404)

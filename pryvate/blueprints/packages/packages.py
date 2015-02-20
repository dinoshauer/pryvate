"""Package blueprint."""
import os

import magic
from flask import Blueprint, current_app, make_response, redirect, request

blueprint = Blueprint('packages', __name__, url_prefix='/packages')


@blueprint.route('/<_>/<__>/<name>/<version>',
                 methods=['GET', 'HEAD'])
def packages(_, __, name, version):
    """Get the contents of a package."""
    filepath = os.path.join(current_app.config['BASEDIR'], name.lower(),
                            version.lower())

    if name in current_app.config['PRIVATE_EGGS']:
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as egg:
                mimetype = magic.from_file(filepath, mime=True)
                contents = egg.read()
                return make_response(contents, 200, {'Content-Type': mimetype})
        return make_response('not found', 404)
    else:
        base_url = current_app.config['PYPI']
        url = base_url.format(request.path)
        return redirect(url, 301)

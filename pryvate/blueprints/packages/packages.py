"""Package blueprint."""
import hashlib
import os

import magic
from flask import (abort, Blueprint, current_app, make_response,
                   render_template, redirect, request)

blueprint = Blueprint('packages', __name__, url_prefix='/packages')


def register_package(name):
    """Register a package."""
    package_path = os.path.join(current_app.config['BASEDIR'], name.lower())
    if not os.path.isdir(package_path):
        os.mkdir(package_path)
    return True


def save_response(name, version, response):
    """Save the contents of a package."""
    egg_path = os.path.join(current_app.config['BASEDIR'], name.lower(),
                            version.lower())
    if not os.path.isfile(egg_path):
        with open(egg_path, 'wb') as egg:
            for block in response.iter_content(1024):
                if not block:
                    break
                egg.write(block)
        with open(egg_path, 'rb') as egg:
            md5 = hashlib.md5(egg.read())
            with open('{}.md5'.format(egg_path), 'w') as digest:
                digest.write(md5.hexdigest())
    return True


@blueprint.route('/<package_type>/<letter>/<name>/<version>',
                 methods=['GET', 'HEAD'])
def packages(package_type, letter, name, version):
    """Get the contents of a package."""
    filepath = os.path.join(current_app.config['BASEDIR'], name.lower(),
                            version.lower())
    remote = request.args.get('remote')

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
        return redirect(url)

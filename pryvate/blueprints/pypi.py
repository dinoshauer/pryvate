"""PyPi blueprint."""
import os
from flask import Blueprint, current_app, request

pypi = Blueprint('pypi', __name__, url_prefix='/pypi')


def register_package(request):
    package_dir = os.path.join(current_app.config['BASEDIR'],
                               request.form['name'].lower())
    if not os.path.isdir(package_dir):
        os.mkdir(package_dir)
    return 'ok'


def upload_package(request):
    contents = request.files['content']
    digest = request.form['md5_digest']
    file_path = os.path.join(current_app.config['BASEDIR'],
                             request.form['name'].lower(),
                             contents.filename.lower())

    contents.save(file_path)
    with open('{}.md5'.format(file_path), 'w') as md5_digest:
        md5_digest.write(digest)
    return 'ok'


@pypi.route('', methods=['POST'])
def post_pypi():
    """Find a package and return the contents of it."""
    actions = {
        'submit': register_package,
        'file_upload': upload_package,
    }
    return actions[request.form[':action']](request)

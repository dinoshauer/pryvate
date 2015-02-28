"""PyPi blueprint."""
import os
from flask import abort, Blueprint, current_app, g, request

blueprint = Blueprint('pypi', __name__, url_prefix='/pypi')


def register_package(localproxy):
    """Register a new package.

    Creates a folder on the filesystem so a new package can be uploaded.

    Arguments:
        localproxy (``werkzeug.local.LocalProxy``): The localproxy object is
            needed to read the ``form`` properties from the request

    Returns:
        ``'ok'``
    """
    package_dir = os.path.join(current_app.config['BASEDIR'],
                               localproxy.form['name'].lower())
    if not os.path.isdir(package_dir):
        os.mkdir(package_dir)
    return 'ok'


def upload_package(localproxy):
    """Save a new package and it's md5 sum in a previously registered path.

    Arguments:
        localproxy (``werkzeug.local.LocalProxy``):The localproxy object is
            needed to read the ``form`` properties from the request

    Returns:
        ``'ok'``
    """
    contents = localproxy.files['content']
    digest = localproxy.form['md5_digest']
    file_path = os.path.join(current_app.config['BASEDIR'],
                             localproxy.form['name'].lower(),
                             contents.filename.lower())

    contents.save(file_path)
    with open('{}.md5'.format(file_path), 'w') as md5_digest:
        md5_digest.write(digest)
    return 'ok'


def get_payload(data):
    """Parse and process a dict for inserting a new egg.

    Necessary because ``request.form`` is an immutable dict.

    Arguments:
        data (``dict`` like object): The object to get values from

    Returns:
        ``dict``
    """
    return {'platform': data['platform'], 'author_email': data['author_email'],
            'name': data['name'].lower(), 'description': data['description'],
            'download_url': data['download_url'], 'summary': data['summary'],
            'version': data['version'], 'home_page': data['home_page'],
            'license': data['license'], 'author': data['author'],
            'metadata_version': data['metadata_version']}


@blueprint.route('', methods=['POST'])
def post_pypi():
    """Find a package and return the contents of it.

    Upon calling this endpoint the ``PRIVATE_EGGS`` set will be updated,
    and proper action will be taken based on the request.
    """
    actions = {
        'submit': register_package,
        'file_upload': upload_package,
    }
    egg_exists = request.form['name'].lower() in g.database.get_eggs_pip()

    if egg_exists:
        return actions[request.form[':action']](request)
    else:
        if request.form[':action'] == 'file_upload':
            data = get_payload(request.form)
            if g.database.new_egg(data):
                return register_package(request)
        return abort(405)

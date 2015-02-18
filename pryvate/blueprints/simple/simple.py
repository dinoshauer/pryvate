"""Simple blueprint."""
import os

from flask import Blueprint, current_app, render_template

blueprint = Blueprint('simple', __name__, url_prefix='/simple',
                   template_folder='templates')


@blueprint.route('', methods=['GET'])
def get_simple():
    """List all packages."""
    packages = os.listdir(current_app.config['BASEDIR'])
    return render_template('simple.html', packages=packages)


@blueprint.route('/<package>', methods=['GET'])
@blueprint.route('/<package>/', methods=['GET'])
def get_package(package):
    """List versions of a package."""
    package_path = os.path.join(current_app.config['BASEDIR'],
                                package.lower())
    files = os.listdir(package_path)

    packages = []
    for filename in files:
        if filename.endswith('md5'):
            with open(os.path.join(package_path, filename), 'r') as md5_digest: 
                item = {
                    'name': package,
                    'version': filename.replace('.md5', ''),
                    'digest': md5_digest.read()
                }
                packages.append(item)
    return render_template('simple_package.html', packages=packages,
                           letter=package[:1].lower())

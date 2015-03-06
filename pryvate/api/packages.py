"""Handle /api/packages for searching etc."""
# pylint: disable=no-init
# pylint: disable=no-self-use
from flask import abort, current_app, g, redirect, url_for
from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse
from fuzzywuzzy import fuzz

parser = reqparse.RequestParser()
parser.add_argument('search', type=str)
parser.add_argument('limit', type=int, default=20, store_missing=True)
parser.add_argument('offset', type=int, default=0, store_missing=True)


class Percentage(fields.Float):

    """A percentage field.

    Sub-classes `flask.ext.restful.fields.Float`
    """

    def format(self, value):
        """Format the value.

        Calls `#super` on ``parent_class#format`

        Returns:
            ``str``: return value of `parent_class#format`
                formatted to as a string with `%`
        """
        value = super(Percentage, self).format(value)
        return '{}%'.format(value)


class PackageList(restful.Resource):

    """Represents a list of packages."""

    RESOURCE_FIELDS = {
        'name': fields.String,
        'description': fields.String,
        'version': fields.String,
        'upload_date': fields.String,
        'probability': Percentage,
        'uri': fields.Url('package'),
    }

    @marshal_with(RESOURCE_FIELDS)
    def get(self):
        """Get a list of packages hosted by pryvate."""
        args = parser.parse_args()
        rows = g.database.get_eggs_api(args['limit'], args['offset'])
        if args.get('search'):
            threshold = current_app.config['SEARCH_RATING_THRESHOLD']
            result = []
            for row in rows:
                row['probability'] = fuzz.ratio(args['search'], row['name'])
                if row['probability'] >= threshold:
                    result.append(row)
            return sorted(result, reverse=True, key=lambda k: k['probability'])
        return rows


class Package(restful.Resource):

    """Represents a single package."""

    VERSION_FIELDS = {
        'upload_date': fields.String,
        'version': fields.String,
    }
    RESOURCE_FIELDS = {
        'author': fields.String,
        'author_email': fields.String,
        'description': fields.String,
        'download_url': fields.String,
        'home_page': fields.String,
        'license': fields.String,
        'metadata_version': fields.String,
        'name': fields.String,
        'platform': fields.String,
        'summary': fields.String,
        'versions': fields.List(fields.Nested(VERSION_FIELDS)),
    }

    @marshal_with(RESOURCE_FIELDS)
    def get(self, name):
        """Get a single package hosted by pryvate."""
        egg = g.database.get_egg_api(name)
        if egg:
            return egg
        abort(404)


class DownloadPackage(restful.Resource):

    """Redirect a request to the download url."""

    def get(self, name, version):
        """Get the download url of a package.

        Arguments:
            name (``str``): Name of the package
            version (``str``): The version of the package

        Returns:
            ``HTTP 302``
        """
        filename = '{}-{}.tar.gz'.format(name, version)
        download_url = url_for('packages.packages', _='_', __='__',
                               name=name, filename=filename)
        return redirect(download_url)

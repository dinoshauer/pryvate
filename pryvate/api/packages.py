"""Handle /api/packages for searching etc."""
# pylint: disable=no-init
# pylint: disable=no-self-use
from flask import current_app, g
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

    def get(self):
        """Pass."""

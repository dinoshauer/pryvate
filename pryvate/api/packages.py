"""Handle /api/packages for searching etc."""
# pylint: disable=no-init
# pylint: disable=no-self-use
from flask import current_app, g
from flask.ext import restful
from flask.ext.restful import reqparse
from fuzzywuzzy import fuzz

parser = reqparse.RequestParser()
parser.add_argument('search', type=str)
parser.add_argument('limit', type=int, default=20, store_missing=True)
parser.add_argument('offset', type=int, default=0, store_missing=True)


class PackageList(restful.Resource):

    """Foo."""

    def get(self):
        """Get a list of packages hosted by pryvate."""
        args = parser.parse_args()
        rows = g.database.get_eggs_api(args['limit'], args['offset'])
        if args.get('search'):
            threshold = current_app.config['SEARCH_RATING_THRESHOLD']
            result = []
            for row in rows:
                row['rating'] = fuzz.ratio(args['search'], row['name'])
                if row['rating'] >= threshold:
                    result.append(row)
            return sorted(result, reverse=True, key=lambda k: k['rating'])
        return rows

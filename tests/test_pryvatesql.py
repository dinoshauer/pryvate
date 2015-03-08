"""PryvateSQL tests."""
# pylint: disable=too-many-public-methods
import unittest

from pryvate.db import PryvateSQLite


class PryvateSQLiteTestCase(unittest.TestCase):

    """Seperate test case for the PryvateSQLite class."""

    def setUp(self):
        """Set up step for all tests."""
        self.pryvate_db = PryvateSQLite(':memory:')

    def tearDown(self):
        """Tear down step, clean up after yourself."""
        self.pryvate_db.connection.close()

    def test_get_eggs(self):
        """Test getting all eggs."""
        expected = []
        result = self.pryvate_db.get_eggs_pip()
        assert result == expected

    def test_new_egg(self):
        """Test creating a new egg."""
        expected = True
        payload = {'description': 'UNKNOWN', 'author': 'UNKNOWN',
                   'home_page': 'UNKNOWN', 'version': '1.0.0',
                   'author_email': 'UNKNOWN', 'license': 'UNKNOWN',
                   'download_url': 'UNKNOWN', 'platform': 'UNKNOWN',
                   'summary': 'Foo.', 'name': 'Foo', 'metadata_version': '1.0'}
        result = self.pryvate_db.new_egg(payload)
        assert result == expected
        expected = {'name': 'Foo'}
        query = self.pryvate_db.GET_ALL_PIP
        result = self.pryvate_db.connection.execute(query)
        for item in result:
            assert dict(item) == expected

    def test_get_eggs_api(self):
        """Test getting all eggs from the API."""
        expected = True
        payload = {'description': 'UNKNOWN', 'author': 'UNKNOWN',
                   'home_page': 'UNKNOWN', 'version': '1.0.0',
                   'author_email': 'UNKNOWN', 'license': 'UNKNOWN',
                   'download_url': 'UNKNOWN', 'platform': 'UNKNOWN',
                   'summary': 'Foo.', 'name': 'Foo', 'metadata_version': '1.0'}
        result = self.pryvate_db.new_egg(payload)
        assert result == expected
        expected = {'version', 'description', 'upload_date', 'name'}
        result = self.pryvate_db.get_eggs_api(1, 0)
        for row in result:
            assert set(row.keys()) == expected


    def test_get_egg_api(self):
        """Test retrieving a single egg from the API."""
        expected = True
        payload = {'description': 'UNKNOWN', 'author': 'UNKNOWN',
                   'home_page': 'UNKNOWN', 'version': '1.0.0',
                   'author_email': 'UNKNOWN', 'license': 'UNKNOWN',
                   'download_url': 'UNKNOWN', 'platform': 'UNKNOWN',
                   'summary': 'Foo.', 'name': 'Foo', 'metadata_version': '1.0'}
        result = self.pryvate_db.new_egg(payload)
        assert result == expected
        expected_keys = {'versions', 'author_email', 'license', 'description',
                         'name', 'summary', 'metadata_version', 'author',
                         'download_url', 'home_page', 'platform'}
        expected_versions = {'upload_date', 'uploader', 'name', 'version'}
        result = self.pryvate_db.get_egg_api('Foo')
        assert set(result.keys()) == expected_keys
        assert type(result['versions']) is list
        assert len(result['versions']) == 1
        for version in result['versions']:
            assert set(version.keys()) == expected_versions

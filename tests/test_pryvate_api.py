"""Pryvate API tests."""
# pylint: disable=too-many-public-methods
# pylint: disable=no-member

import json
import os
import unittest
import shutil
import tempfile

import pryvate
from pryvate.api.packages import Percentage
from pryvate.db import PryvateSQLite


def test_percentage_field():
    """Test that the Percentage class works as expected."""
    expected = [(20, '20.0%'), (11.2, '11.2%')]
    for value, expected in expected:
        assert Percentage().format(value) == expected

class PryvateAPITestCase(unittest.TestCase):

    """Main test case for Pryvate's API."""

    @staticmethod
    def _copy_egg(tempdir):
        """Copy the files from res/meep to {tempdir}/meep."""
        base = 'tests/res/meep'
        os.mkdir(os.path.join(tempdir, 'meep'))
        for item in os.listdir(base):
            shutil.copyfile(
                os.path.join(base, item),
                os.path.join(tempdir, 'meep', item),
            )

    def setUp(self):
        """Set up step for all tests."""
        self.egg_folder = tempfile.mkdtemp()
        _, self.db_path = tempfile.mkstemp()
        self._copy_egg(self.egg_folder)
        pryvate.server.app.testing = True
        pryvate.server.app.config['BASEDIR'] = self.egg_folder
        pryvate.server.app.config['DB_PATH'] = self.db_path
        self.database = PryvateSQLite(self.db_path)
        data = {'description': 'UNKNOWN', 'author': 'UNKNOWN',
                'home_page': 'UNKNOWN', 'version': '1.0.0',
                'author_email': 'UNKNOWN', 'license': 'UNKNOWN',
                'download_url': 'UNKNOWN', 'platform': 'UNKNOWN',
                'summary': 'Meep.', 'name': 'meep', 'metadata_version': '1.0'}
        self.database.new_egg(data)
        self.app = pryvate.server.app.test_client()
        self.packages = '/api/packages'
        self.package = '/api/package/{name}'
        self.download = '/api/package/{name}/download/{version}'

    def tearDown(self):
        """Tear down stop for all tests."""
        self.database.connection.close()
        os.unlink(self.db_path)
        shutil.rmtree(self.egg_folder)

    def test_package_list(self):
        """Test GET /api/packages."""
        request = self.app.get(self.packages)
        assert request.status_code == 200
        result = json.loads(request.data.decode())
        expected_keys = {'description', 'uri', 'version', 'upload_date', 'name',
                         'probability'}
        for row in result:
            assert set(row.keys()) == expected_keys

    def test_package_list_search(self):
        """Test GET /api/packages?search=meep."""
        request = self.app.get(self.packages, data={'search': 'meep'})
        result = json.loads(request.data.decode())
        for row in result:
            assert row['probability'] is not None

    def test_package(self):
        """Test GET /api/package/meep."""
        request = self.app.get(self.package.format(name='meep'))
        assert request.status_code == 200
        result = json.loads(request.data.decode())
        expected_keys = {'download_url', 'metadata_version', 'author',
                         'description', 'license', 'summary', 'name',
                         'author_email', 'versions', 'platform', 'home_page'}
        assert set(result.keys()) == expected_keys
        assert type(result['versions']) is list
        assert len(result['versions']) == 1
        expected_versions = {'upload_date', 'uri', 'version'}
        for version in result['versions']:
            print(version)
            assert set(version.keys()) == expected_versions
            expected = '/api/package/meep/download/{version}'.format(
                version=version['version'],
            )
            assert version['uri'] == expected

    def test_package_404(self):
        """Test 404 GET /api/package/foo."""
        request = self.app.get(self.package.format(name='foo'))
        assert request.status_code == 404

    def test_download_packacge(self):
        """Test GET /api/package/meep/download/1.0.0."""
        request = self.app.get(self.download.format(name='meep',
                                                    version='1.0.0'))
        expected = '/packages/_/__/meep/meep-1.0.0.tar.gz'
        assert request.status_code == 302
        assert expected in request.headers['Location']

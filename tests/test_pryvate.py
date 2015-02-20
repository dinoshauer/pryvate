"""Pryvate tests."""
# pylint: disable=too-many-public-methods
# pylint: disable=no-member

import os
import unittest
import shutil
import tempfile

from bs4 import BeautifulSoup

import pryvate


class PryvateTestCase(unittest.TestCase):

    """Main test case for Pryvate."""

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
        self.egg_folder = tempfile.TemporaryDirectory()
        self._copy_egg(self.egg_folder.name)
        pryvate.server.app.config['BASEDIR'] = self.egg_folder.name
        pryvate.server.app.config['PRIVATE_EGGS'] = {'meep'}
        self.app = pryvate.server.app.test_client()
        self.simple = '/simple'

    def tearDown(self):
        """Tear down stop for all tests."""
        self.egg_folder.cleanup()

    def test_search(self):
        """Assert that the search feature is not implemented."""
        request = self.app.post(self.simple)
        assert request.status_code == 501
        assert request.data == b'Not implemented'

    def test_get_all(self):
        """Assert that pryvate can return a list of packages."""
        expected = 'meep'
        request = self.app.get(self.simple)
        response = BeautifulSoup(request.data)
        assert request.status_code == 200
        assert expected in [a.string for a in response.find_all('a')]

    def test_get_private_egg(self):
        """Assert that pryvate will return a privately registered egg."""
        expected = 'meep-1.0.0.tar.gz'
        request = self.app.get('{}/meep/'.format(self.simple))
        response = BeautifulSoup(request.data)
        assert request.status_code == 200
        assert expected in [a.string for a in response.find_all('a')]

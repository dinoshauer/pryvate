"""Pryvate tests."""

import os
import unittest
import shutil
import tempfile

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
        self.app = pryvate.server.app.test_client()

    def tearDown(self):
        """Tear down stop for all tests."""
        self.egg_folder.cleanup()

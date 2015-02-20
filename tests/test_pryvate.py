"""Pryvate tests."""

import os
import unittest
import shutil
import tempfile

import pryvate


class PryvateTestCase(unittest.TestCase):

    """Main test case for Pryvate."""

    def setUp(self):
        """Set up step for all tests."""
        self.egg_folder = tempfile.TemporaryDirectory()
        pryvate.server.app.config['BASEDIR'] = self.egg_folder.name
        self.app = pryvate.server.app.test_client()

    def tearDown(self):
        """Tear down stop for all tests."""
        self.egg_folder.cleanup()

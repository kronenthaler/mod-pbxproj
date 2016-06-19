import shutil
import unittest
import os

from pbxproj import *
from pbxproj import XcodeProject


class XCodeProjectTest(unittest.TestCase):
    def setUp(self):
        # create tmp directory for results
        if not os.path.exists("results"):
            os.mkdir("results")

    def tearDown(self):
        # remove tmp directory
        shutil.rmtree('results')

    def testSaveOnGivenPath(self):
        XcodeProject().save("results/sample")

        self.assertTrue(os.path.exists("results/sample"))

    def testSaveOnDefaultPath(self):
        XcodeProject({}, "results/default").save()

        self.assertTrue(os.path.exists("results/default"))

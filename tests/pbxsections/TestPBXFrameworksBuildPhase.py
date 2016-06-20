import unittest
from pbxproj.pbxsections.PBXFrameworksBuildPhase import *


class PBXFrameworksBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXFrameworksBuildPhase()
        self.assertEqual(obj._get_comment(), u'Frameworks')

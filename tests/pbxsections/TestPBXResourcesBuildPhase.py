import unittest
from pbxproj.pbxsections.PBXResourcesBuildPhase import *


class PBXResourcesBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXResourcesBuildPhase()
        self.assertEqual(obj._get_comment(), u'Resources')

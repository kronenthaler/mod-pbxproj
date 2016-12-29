import unittest
from pbxproj.pbxsections.PBXHeadersBuildPhase import *


class PBXHeadersBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXHeadersBuildPhase()
        self.assertEqual(obj._get_comment(), u'Headers')

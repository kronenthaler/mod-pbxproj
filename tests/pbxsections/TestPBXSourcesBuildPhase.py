import unittest
from pbxproj.pbxsections.PBXSourcesBuildPhase import *


class PBXSourcesBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXSourcesBuildPhase()
        self.assertEqual(obj._get_comment(), u'Sources')

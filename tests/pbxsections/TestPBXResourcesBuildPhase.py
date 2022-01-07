import unittest

from pbxproj.pbxsections import PBXResourcesBuildPhase


class PBXResourcesBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXResourcesBuildPhase()
        self.assertEqual(obj._get_comment(), u'Resources')

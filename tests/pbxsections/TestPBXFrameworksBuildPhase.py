import unittest

from pbxproj import PBXFrameworksBuildPhase


class PBXFrameworksBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXFrameworksBuildPhase()
        self.assertEqual(obj._get_comment(), u'Frameworks')

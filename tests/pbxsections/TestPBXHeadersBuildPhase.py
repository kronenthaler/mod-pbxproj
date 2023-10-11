import unittest

from pbxproj import PBXHeadersBuildPhase


class PBXHeadersBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXHeadersBuildPhase()
        assert obj._get_comment() == u'Headers'

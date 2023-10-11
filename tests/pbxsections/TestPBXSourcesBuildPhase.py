import unittest

from pbxproj.pbxsections.PBXSourcesBuildPhase import PBXSourcesBuildPhase


class PBXSourcesBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXSourcesBuildPhase()
        assert obj._get_comment() == u'Sources'

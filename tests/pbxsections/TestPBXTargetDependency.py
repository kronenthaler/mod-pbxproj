import unittest

from pbxproj.pbxsections.PBXTargetDependency import PBXTargetDependency


class PBXTargetDependencyTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXTargetDependency()
        assert obj._get_comment() == u'PBXTargetDependency'

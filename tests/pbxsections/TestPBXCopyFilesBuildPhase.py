import unittest

from pbxproj.pbxsections.PBXCopyFilesBuildPhase import PBXCopyFilesBuildPhase


class PBXCopyFilesBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        phase = PBXCopyFilesBuildPhase()
        self.assertEqual(phase._get_comment(), "CopyFiles")

    def testGetCommentFromParent(self):
        phase = PBXCopyFilesBuildPhase()
        phase.name = "copy"
        self.assertEqual(phase._get_comment(), "copy")

import unittest

from pbxproj.pbxsections.PBXShellScriptBuildPhase import PBXShellScriptBuildPhase


class PBXShellScriptBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXShellScriptBuildPhase()
        self.assertEqual(obj._get_comment(), u'ShellScript')

    def testGetCommentWithName(self):
        name = u'Run My Script Please'
        obj = PBXShellScriptBuildPhase.create(script=u'/dev/null', name=name)
        self.assertEqual(obj._get_comment(), name)

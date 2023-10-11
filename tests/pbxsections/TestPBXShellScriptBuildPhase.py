import unittest

from pbxproj.pbxsections.PBXShellScriptBuildPhase import PBXShellScriptBuildPhase


class PBXShellScriptBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXShellScriptBuildPhase()
        assert obj._get_comment() == u'ShellScript'

    def testGetCommentWithName(self):
        name = u'Run My Script Please'
        obj = PBXShellScriptBuildPhase.create(script=u'/dev/null', name=name)
        assert obj._get_comment() == name

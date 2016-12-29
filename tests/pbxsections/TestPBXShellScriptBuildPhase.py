import unittest
from pbxproj.pbxsections.PBXShellScriptBuildPhase import *


class PBXShellScriptBuildPhaseTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXShellScriptBuildPhase()
        self.assertEqual(obj._get_comment(), u'ShellScript')

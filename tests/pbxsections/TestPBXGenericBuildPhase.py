import unittest
from pbxproj.pbxsections.PBXGenericBuildPhase import *


class PBXGenericBuildPhaseTest(unittest.TestCase):
    def testAddBuildFile(self):
        build_phase = PBXGenericBuildPhase.create(name="build_phase")
        result = build_phase.add_build_file(PBXGenericObject().parse({}))

        self.assertFalse(result)
        self.assertListEqual(build_phase.files, [])

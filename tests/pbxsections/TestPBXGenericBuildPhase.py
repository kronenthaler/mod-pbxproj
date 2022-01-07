import unittest

from pbxproj import PBXGenericBuildPhase, PBXGenericObject


class PBXGenericBuildPhaseTest(unittest.TestCase):
    def testAddBuildFile(self):
        build_phase = PBXGenericBuildPhase.create(name="build_phase")
        result = build_phase.add_build_file(PBXGenericObject().parse({}))

        self.assertFalse(result)
        self.assertListEqual(build_phase.files, [])

    def testRemoveBuildFileFailed(self):
        build_phase = PBXGenericBuildPhase.create(name="build_phase")
        build_phase.add_build_file(PBXGenericObject().parse({}))

        result = build_phase.remove_build_file(None)

        self.assertFalse(result)
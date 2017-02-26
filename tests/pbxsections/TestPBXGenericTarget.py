import unittest
from pbxproj.XcodeProject import *


class PBXGenericTargetTest(unittest.TestCase):
    def testGetBuildPhase(self):
        project = XcodeProject({
            "objects": {
                "1": {"isa": "PBXGenericTarget", "buildPhases": ["2"]},
                "2": {"isa": "PBXGenericBuildPhase"}
            }
        })

        build_phases = project.objects['1'].get_or_create_build_phase("PBXGenericBuildPhase")

        self.assertListEqual(build_phases, [project.objects["2"]])

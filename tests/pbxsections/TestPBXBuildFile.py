import unittest

from pbxproj.pbxsections.PBXBuildFile import PBXBuildFile
from pbxproj.XcodeProject import XcodeProject


class PBXBuildFileTest(unittest.TestCase):
    def testPrintOnSingleLine(self):
        obj = {"isa": "PBXBuildFile", "name": "something"}
        dobj = PBXBuildFile().parse(obj)

        self.assertEqual(dobj.__repr__(), "{isa = PBXBuildFile; name = something; }")

    def testGetComment(self):
        obj = {
            'objects': {
                '1': {"isa": "PBXBuildFile", "name": "something", 'fileRef': 'FDDF6A571C68E5B100D7A645'},
                'FDDF6A571C68E5B100D7A645': {'isa': 'PBXFileReference', "name": "real name"},
                "X": {'isa':'phase', 'name': 'X', 'files': ['1'] }
            }
        }
        dobj = XcodeProject().parse(obj)

        self.assertEqual(dobj.objects['1']._get_comment(), "real name in X")
import unittest

from pbxproj.pbxsections.PBXBuildFile import PBXBuildFile
from pbxproj.PBXGenericObject import PBXGenericObject
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
                "X": {'isa': 'phase', 'name': 'X', 'files': ['1']}
            }
        }
        dobj = XcodeProject().parse(obj)

        self.assertEqual(dobj.objects['1']._get_comment(), "real name in X")

    def testAddAttributesWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.add_attributes(u'Weak')

        self.assertIsNotNone(dobj.settings.ATTRIBUTES)
        self.assertEquals(dobj.settings.ATTRIBUTES, [u'Weak'])

    def testAddAttributesWithoutAttributes(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags="x")

        dobj.add_attributes(u'Weak')

        self.assertIsNotNone(dobj.settings.ATTRIBUTES)
        self.assertEquals(dobj.settings.ATTRIBUTES, [u'Weak'])

    def testAddAttributesWithAttributes(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), attributes="x")
        dobj.add_attributes(u'Weak')

        self.assertIsNotNone(dobj.settings.ATTRIBUTES)
        self.assertEquals(dobj.settings.ATTRIBUTES, [u'x', u'Weak'])

    def testRemoveAttributesWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.remove_attributes('Weak')

        self.assertIsNone(dobj[u'settings'])

    def testRemoveAttributesWithSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), attributes=["Weak"])

        dobj.remove_attributes('Weak')

        self.assertIsNone(dobj[u'settings'])

    def testAddCompilerFlagWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.add_compiler_flags([u'Weak', '-fno-arc'])

        self.assertIsNotNone(dobj.settings.COMPILER_FLAGS)
        self.assertEquals(dobj.settings.COMPILER_FLAGS, u'Weak -fno-arc')

    def testAddCompilerFlagWithFlags(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags=[u'Weak', '-fno-arc'])

        dobj.add_compiler_flags('x')

        self.assertIsNotNone(dobj.settings.COMPILER_FLAGS)
        self.assertEquals(dobj.settings.COMPILER_FLAGS, u'Weak -fno-arc x')

    def testRemoveCompilerFlagsWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.remove_compiler_flags('Weak')

        self.assertIsNone(dobj[u'settings'])

    def testRemoveCompilerFlagsWithSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags=u'Weak')

        dobj.remove_compiler_flags('Weak')

        self.assertIsNone(dobj[u'settings'])

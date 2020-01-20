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
                '1': {'isa': 'PBXBuildFile', 'name': 'something', 'fileRef': 'FDDF6A571C68E5B100D7A645'},
                'FDDF6A571C68E5B100D7A645': {'isa': 'PBXFileReference', 'name': 'real name'},
                'X': {'isa': 'phase', 'name': 'X', 'files': ['1']}
            }
        }
        dobj = XcodeProject().parse(obj)

        self.assertEqual(dobj.objects['1']._get_comment(), 'real name in X')

    def testGetAttributesWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        attributes = dobj.get_attributes()

        self.assertIsNone(attributes)

    def testGetAttributesWithoutAttributes(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags='x')

        attributes = dobj.get_attributes()

        self.assertIsNone(attributes)

    def testGetAttributesWithAttributes(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), attributes='x')

        attributes = dobj.get_attributes()

        self.assertIsNotNone(attributes)
        self.assertEqual(attributes, ['x'])

    def testGetCompilerFlagsWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        self.assertIsNone(dobj.get_compiler_flags())

    def testGetCompilerFlagsWithoutFlags(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), attributes='x')

        self.assertIsNone(dobj.get_compiler_flags())

    def testGetCompilerFlagsWithFlags(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags=['Weak', '-fno-arc'])

        self.assertIsNotNone(dobj.get_compiler_flags())
        self.assertEqual(dobj.get_compiler_flags(), 'Weak -fno-arc')

    def testGetCommentForNonExistentRef(self):
        obj = {
            'objects': {
                'FDDF6A571C68E5B100D7A645': {'isa': 'PBXBuildFile'},
                'X': {'isa': 'phase', 'name': 'X', 'files': ['FDDF6A571C68E5B100D7A645']}
            }
        }
        dobj = XcodeProject().parse(obj)

        self.assertEqual(dobj.objects['FDDF6A571C68E5B100D7A645']._get_comment(), '(null) in X')

    def testAddAttributesWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.add_attributes('Weak')

        self.assertIsNotNone(dobj.settings.ATTRIBUTES)
        self.assertEqual(dobj.settings.ATTRIBUTES, ['Weak'])

    def testAddAttributesWithoutAttributes(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags='x')

        dobj.add_attributes('Weak')

        self.assertIsNotNone(dobj.settings.ATTRIBUTES)
        self.assertEqual(dobj.settings.ATTRIBUTES, ['Weak'])

    def testAddAttributesWithAttributes(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), attributes='x')
        dobj.add_attributes('Weak')

        self.assertIsNotNone(dobj.settings.ATTRIBUTES)
        self.assertEqual(dobj.settings.ATTRIBUTES, ['x', 'Weak'])

    def testRemoveAttributesWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.remove_attributes('Weak')

        self.assertIsNone(dobj['settings'])

    def testRemoveAttributesWithSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), attributes=['Weak'])

        dobj.remove_attributes('Weak')

        self.assertIsNone(dobj['settings'])

    def testAddCompilerFlagWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.add_compiler_flags(['Weak', '-fno-arc'])

        self.assertIsNotNone(dobj.settings.COMPILER_FLAGS)
        self.assertEqual(dobj.settings.COMPILER_FLAGS, 'Weak -fno-arc')

    def testAddCompilerFlagWithFlags(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags=['Weak', '-fno-arc'])

        dobj.add_compiler_flags('x')

        self.assertIsNotNone(dobj.settings.COMPILER_FLAGS)
        self.assertEqual(dobj.settings.COMPILER_FLAGS, 'Weak -fno-arc x')

    def testRemoveCompilerFlagsWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.remove_compiler_flags('Weak')

        self.assertIsNone(dobj['settings'])

    def testRemoveCompilerFlagsWithSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags='Weak')

        dobj.remove_compiler_flags('Weak')

        self.assertIsNone(dobj['settings'])

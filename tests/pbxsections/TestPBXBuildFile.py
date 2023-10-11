import unittest

from pbxproj.PBXGenericObject import PBXGenericObject
from pbxproj.XcodeProject import XcodeProject
from pbxproj.pbxsections.PBXBuildFile import PBXBuildFile


class PBXBuildFileTest(unittest.TestCase):
    def testPrintOnSingleLine(self):
        obj = {"isa": "PBXBuildFile", "name": "something"}
        dobj = PBXBuildFile().parse(obj)

        assert dobj.__repr__() == "{isa = PBXBuildFile; name = something; }"

    def testGetComment(self):
        obj = {
            'objects': {
                '1': {'isa': 'PBXBuildFile', 'name': 'something', 'fileRef': 'FDDF6A571C68E5B100D7A645'},
                'FDDF6A571C68E5B100D7A645': {'isa': 'PBXFileReference', 'name': 'real name'},
                'X': {'isa': 'phase', 'name': 'X', 'files': ['1']}
            }
        }
        dobj = XcodeProject().parse(obj)

        assert dobj.objects['1']._get_comment() == 'real name in X'

    def testGetAttributesWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        attributes = dobj.get_attributes()

        assert attributes is None

    def testGetAttributesWithoutAttributes(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags='x')

        attributes = dobj.get_attributes()

        assert attributes is None

    def testGetAttributesWithAttributes(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), attributes='x')

        attributes = dobj.get_attributes()

        assert attributes is not None
        assert attributes == ['x']

    def testGetCompilerFlagsWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        assert dobj.get_compiler_flags() is None

    def testGetCompilerFlagsWithoutFlags(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), attributes='x')

        assert dobj.get_compiler_flags() is None

    def testGetCompilerFlagsWithFlags(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags=['Weak', '-fno-arc'])

        assert dobj.get_compiler_flags() is not None
        assert dobj.get_compiler_flags() == 'Weak -fno-arc'

    def testGetCommentForNonExistentRef(self):
        obj = {
            'objects': {
                'FDDF6A571C68E5B100D7A645': {'isa': 'PBXBuildFile'},
                'X': {'isa': 'phase', 'name': 'X', 'files': ['FDDF6A571C68E5B100D7A645']}
            }
        }
        dobj = XcodeProject().parse(obj)

        assert dobj.objects['FDDF6A571C68E5B100D7A645']._get_comment() == '(null) in X'

    def testAddAttributesWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.add_attributes('Weak')

        assert dobj.settings.ATTRIBUTES is not None
        assert dobj.settings.ATTRIBUTES == ['Weak']

    def testAddAttributeList(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.add_attributes(['Weak', 'Custom'])

        assert dobj.settings.ATTRIBUTES is not None
        assert dobj.settings.ATTRIBUTES == ['Weak', 'Custom']

    def testAddAttributesWithoutAttributes(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags='x')

        dobj.add_attributes('Weak')

        assert dobj.settings.ATTRIBUTES is not None
        assert dobj.settings.ATTRIBUTES == ['Weak']

    def testAddAttributesWithAttributes(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), attributes='x')
        dobj.add_attributes('Weak')

        assert dobj.settings.ATTRIBUTES is not None
        assert dobj.settings.ATTRIBUTES == ['x', 'Weak']

    def testRemoveAttributesWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.remove_attributes('Weak')

        assert dobj['settings'] is None

    def testRemoveAttributeList(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), attributes=['Weak', 'Custom'])

        dobj.remove_attributes(['Weak', 'Custom'])

        assert dobj['settings'] is None

    def testRemoveAttributesWithSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), attributes=['Weak'])

        dobj.remove_attributes('Weak')

        assert dobj['settings'] is None

    def testAddCompilerFlagWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.add_compiler_flags(['Weak', '-fno-arc'])

        assert dobj.settings.COMPILER_FLAGS is not None
        assert dobj.settings.COMPILER_FLAGS == 'Weak -fno-arc'

    def testAddCompilerFlagWithFlags(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags=['Weak', '-fno-arc'])

        dobj.add_compiler_flags('x')

        assert dobj.settings.COMPILER_FLAGS is not None
        assert dobj.settings.COMPILER_FLAGS == 'Weak -fno-arc x'

    def testRemoveCompilerFlagsWithoutSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject())

        dobj.remove_compiler_flags('Weak')

        assert dobj['settings'] is None

    def testRemoveCompilerFlagsWithSettings(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags='Weak')

        dobj.remove_compiler_flags('Weak')

        assert dobj['settings'] is None

    def testRemoveCompilerFlagsList(self):
        dobj = PBXBuildFile.create(PBXGenericObject(), compiler_flags=['Weak', 'Custom', 'Another'])

        dobj.remove_compiler_flags(['Weak', 'Custom'])

        assert dobj['settings'] is not None
        assert dobj['settings'].__repr__() == PBXGenericObject().parse({'COMPILER_FLAGS': 'Another'}).__repr__()

    def testRemoveNonRecursive(self):
        obj = {
            'objects': {
                '1': {'isa': 'PBXBuildFile', 'fileRef': '0'},
                '0': {'isa': 'PBXFileReference', 'path': 'x'},
                '2': {'isa': 'PBXGenericBuildPhase', 'files': ['1']}
            }
        }

        project = PBXGenericObject().parse(obj)
        project.objects['1'].remove(recursive=False)

        assert project.objects['1'] is None
        assert project.objects['2'] is not None

    def testGetCommentOfProduct(self):
        obj = {
            'objects': {
                '1': {'isa': 'PBXBuildFile', 'productRef': 'FDDF6A571C68E5B100D7A645'},
                'FDDF6A571C68E5B100D7A645': {'isa': 'PBXFileReference', 'name': 'real name'},
                'X': {'isa': 'phase', 'name': 'X', 'files': ['1']}
            }
        }
        dobj = XcodeProject().parse(obj)

        assert dobj.objects['1']._get_comment() == 'real name in X'

    def testPrintFile(self):
        obj = {"isa": "PBXBuildFile", "fileRef": "X" }
        dobj = PBXBuildFile().parse(obj)

        assert dobj.__repr__() == "{isa = PBXBuildFile; fileRef = X; }"

    def testPrintProduct(self):
        obj = {"isa": "PBXBuildFile", "productRef": "X" }
        dobj = PBXBuildFile().parse(obj)

        assert dobj.__repr__() == "{isa = PBXBuildFile; productRef = X; }"

    def testIsFile(self):
        obj = PBXGenericObject().parse({"_id": "1" })
        dobj = PBXBuildFile.create(obj)

        assert hasattr(dobj, "fileRef")

    def testIsProduct(self):
        obj = PBXGenericObject().parse({"_id": "1" })
        dobj = PBXBuildFile.create(obj, is_product=True)

        assert hasattr(dobj, "productRef")

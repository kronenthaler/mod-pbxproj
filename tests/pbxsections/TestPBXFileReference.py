import unittest

from pbxproj.pbxsections.PBXFileReference import PBXFileReference


class PBXFileReferenceTest(unittest.TestCase):
    def testPrintOnSingleLine(self):
        obj = {"isa": "PBXFileReference", "name": "something"}
        dobj = PBXFileReference().parse(obj)

        assert dobj.__repr__() == "{isa = PBXFileReference; name = something; }"

    def testSetLastKnownType(self):
        dobj = PBXFileReference.create("path")

        dobj.set_last_known_file_type('something')

        assert dobj.lastKnownFileType == "something"
        assert dobj['explicitFileType'] is None

    def testSetExplicityFileType(self):
        dobj = PBXFileReference.create("path")

        dobj.set_explicit_file_type('something')

        assert dobj.explicitFileType == "something"
        assert dobj['lastKnownFileType'] is None

    def testSetLastTypeRemovesExplicit(self):
        dobj = PBXFileReference.create("path")

        dobj.set_explicit_file_type('something')
        dobj.set_last_known_file_type('something')

        assert dobj.lastKnownFileType == "something"
        assert dobj['explicitFileType'] is None

    def testSetExplicitRemovesLastType(self):
        dobj = PBXFileReference.create("path")

        dobj.set_last_known_file_type('something')
        dobj.set_explicit_file_type('something')

        assert dobj.explicitFileType == "something"
        assert dobj['lastKnownFileType'] is None

import unittest

from pbxproj.pbxsections.PBXFileReference import PBXFileReference


class PBXFileReferenceTest(unittest.TestCase):
    def testPrintOnSingleLine(self):
        obj = {"isa": "PBXFileReference", "name": "something"}
        dobj = PBXFileReference().parse(obj)

        self.assertEqual(dobj.__repr__(), "{isa = PBXFileReference; name = something; }")

    def testSetLastKnownType(self):
        dobj = PBXFileReference.create("path")

        dobj.set_last_known_file_type('something')

        self.assertEqual(dobj.lastKnownFileType, "something")
        self.assertIsNone(dobj['explicitFileType'])

    def testSetExplicityFileType(self):
        dobj = PBXFileReference.create("path")

        dobj.set_explicit_file_type('something')

        self.assertEqual(dobj.explicitFileType, "something")
        self.assertIsNone(dobj['lastKnownFileType'])

    def testSetLastTypeRemovesExplicit(self):
        dobj = PBXFileReference.create("path")

        dobj.set_explicit_file_type('something')
        dobj.set_last_known_file_type('something')

        self.assertEqual(dobj.lastKnownFileType, "something")
        self.assertIsNone(dobj['explicitFileType'])

    def testSetExplicitRemovesLastType(self):
        dobj = PBXFileReference.create("path")

        dobj.set_last_known_file_type('something')
        dobj.set_explicit_file_type('something')

        self.assertEqual(dobj.explicitFileType, "something")
        self.assertIsNone(dobj['lastKnownFileType'])

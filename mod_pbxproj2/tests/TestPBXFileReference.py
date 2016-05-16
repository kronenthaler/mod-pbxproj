import unittest
from mod_pbxproj2 import *


class PBXFileReferenceTest(unittest.TestCase):
    def testPrintOnSingleLine(self):
        obj = {"isa": "PBXFileReference", "name": "something"}
        dobj = PBXFileReference().parse(obj)

        self.assertEqual(dobj.__repr__(), "{isa = PBXFileReference; name = something; }")
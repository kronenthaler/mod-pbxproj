import unittest
from mod_pbxproj2 import *


class PBXBuildFileTest(unittest.TestCase):
    def testPrintOnSingleLine(self):
        obj = {"isa": "PBXBuildFile", "name": "something"}
        dobj = PBXBuildFile().parse(obj)

        self.assertEqual(dobj.__repr__(), "{isa = PBXBuildFile; name = something; }")
import unittest
from pbxproj.pbxsections.XCLocalSwiftPackageReference import *


class TestXCLocalSwiftPackageReference(unittest.TestCase):
    def testGetComment(self):
        obj = XCLocalSwiftPackageReference.create('MyPackage')
        assert obj._get_comment() == 'XCLocalSwiftPackageReference "MyPackage"'

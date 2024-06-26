import unittest
from pbxproj.pbxsections.XCSwiftPackageProductDependency import *


class TestXCSwiftPackageProductDependency(unittest.TestCase):
    def testGetComment(self):
        obj = PBXGenericObject()
        dobj = XCSwiftPackageProductDependency.create(obj, 'Some Product')
        assert dobj._get_comment() == 'Some Product'

    def testPackageIsNotNone(self):
        obj = PBXGenericObject().parse({"_id": "1" })
        dobj = XCSwiftPackageProductDependency.create(obj, 'Some Product')
        assert dobj['package'] is not None

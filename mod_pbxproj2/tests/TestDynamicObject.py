import unittest
from mod_pbxproj2 import *
import openstep_parser as osp


class DynamicObjectTest(unittest.TestCase):
    def testParseCreateAttributes(self):
        obj = {"a": "varA", "b": [1, 2, 3], "c": {"c1": "varC1"}}
        dobj = DynamicObject().parse(obj)
        self.assertEqual(dobj.a, "varA")
        self.assertEqual(dobj.b, [1, 2, 3])
        self.assertIsNotNone(dobj.c)

    def testParseCreateObjectOfRightTypes(self):
        obj = {"objects": {"id": {"isa": "type"}}}
        dobj = DynamicObject().parse(obj)

        self.assertEqual(type(dobj.objects), objects)

    def testEscapeItem(self):
        self.assertEqual(DynamicObject._escape("/bin/sh"), "/bin/sh")
        self.assertEqual(DynamicObject._escape("abcdefghijklmnopqrstuvwyz0123456789"), "abcdefghijklmnopqrstuvwyz0123456789")
        self.assertEqual(DynamicObject._escape("some spaces"), '"some spaces"')
        self.assertEqual(DynamicObject._escape("a-valid_id."), "a-valid_id.")
        self.assertEqual(DynamicObject._escape("<group>"), '"<group>"')

    def testPrintObject(self):
        obj = {"a": "varA", "b": [1, 2, 3], "c": {"c1": "varC1"}}
        dobj = DynamicObject().parse(obj)
        expected = '{\n\ta = varA;\n\tb = (\n\t\t1,\n\t\t2,\n\t\t3,\n\t);\n\tc = {\n\t\tc1 = varC1;\n\t};\n}'

        self.assertEqual(dobj.__repr__(), expected)


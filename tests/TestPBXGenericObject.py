import unittest

from pbxproj import PBXGenericObject
from pbxproj.PBXObjects import objects
from pbxproj.PBXKey import PBXKey


class PBXGenericObjectTest(unittest.TestCase):
    def testParseCreateAttributes(self):
        obj = {"a": "varA", "b": [1, 2, 3], "c": {"c1": "varC1"}}
        dobj = PBXGenericObject().parse(obj)
        self.assertEqual(dobj.a, "varA")
        self.assertEqual(dobj.b, [1, 2, 3])
        self.assertIsNotNone(dobj.c)

    def testParseCreateObjectOfRightTypes(self):
        obj = {"objects": {"id": {"isa": "type"}}}
        dobj = PBXGenericObject().parse(obj)

        self.assertIsInstance(dobj.objects, objects)

    def testParseKey(self):
        obj = "FDDF6A571C68E5B100D7A645"
        dobj = PBXGenericObject().parse(obj)

        self.assertIsInstance(dobj, PBXKey)

    def testEscapeItem(self):
        self.assertEqual(PBXGenericObject._escape("/bin/sh"), "/bin/sh")
        self.assertEqual(PBXGenericObject._escape("abcdefghijklmnopqrstuvwyz0123456789"),
                         "abcdefghijklmnopqrstuvwyz0123456789")
        self.assertEqual(PBXGenericObject._escape("some spaces"), '"some spaces"')
        self.assertEqual(PBXGenericObject._escape("a.valid_id."), "a.valid_id.")
        self.assertEqual(PBXGenericObject._escape("a-invalid-id"), '"a-invalid-id"')
        self.assertEqual(PBXGenericObject._escape("<group>"), '"<group>"')
        self.assertEqual(PBXGenericObject._escape("script \\ continuation"), '"script \\\\ continuation"')
        self.assertEqual(PBXGenericObject._escape("/bin/sh find .. -name '*.framework'", exclude=["\'"]),
                         "\"/bin/sh find .. -name '*.framework'\"")

    def testPrintObject(self):
        obj = {"a": "varA", "b": [1, 2, 3], "c": {"c1": "FDDF6A571C68E5B100D7A645"}}
        dobj = PBXGenericObject().parse(obj)

        expected = '{\n\ta = varA;\n\tb = (\n\t\t1,\n\t\t2,\n\t\t3,\n\t);\n\tc = {\n\t\tc1 = FDDF6A571C68E5B100D7A645;\n\t};\n}'

        self.assertEqual(dobj.__repr__(), expected)

    def testGetItem(self):
        obj = {"a": "varA", "b": [1, 2, 3], "c": {"c1": "FDDF6A571C68E5B100D7A645"}}
        dobj = PBXGenericObject().parse(obj)

        self.assertIsInstance(dobj["c"]["c1"], PBXKey)
        self.assertIsNone(dobj['X'])

    def testSetItemNone(self):
        obj = {}
        dobj = PBXGenericObject().parse(obj)

        self.assertIsNone(dobj['something'])

        dobj['something'] = None
        self.assertIsNone(dobj['something'])

    def testSetItemString(self):
        obj = {}
        dobj = PBXGenericObject().parse(obj)

        self.assertIsNone(dobj['something'])

        dobj['something'] = 'yes'
        self.assertEqual(dobj['something'], 'yes')

    def testSetItemListOfZero(self):
        obj = {}
        dobj = PBXGenericObject().parse(obj)

        self.assertIsNone(dobj['something'])

        dobj['something'] = []
        self.assertIsNone(dobj['something'])

    def testSetItemListOfOne(self):
        obj = {}
        dobj = PBXGenericObject().parse(obj)

        self.assertIsNone(dobj['something'])

        dobj['something'] = ['yes']
        self.assertEqual(dobj['something'], 'yes')

    def testSetItemListOfTwo(self):
        obj = {}
        dobj = PBXGenericObject().parse(obj)

        self.assertIsNone(dobj['something'])

        dobj['something'] = ['yes', 'yes']
        self.assertEqual(dobj['something'], ['yes', 'yes'])

    def testResolveComment(self):
        obj = {"a": {"name": "A"}, "b": {"path": "B"}, "c": {"c1": "FDDF6A571C68E5B100D7A645"}}
        dobj = PBXGenericObject().parse(obj)

        self.assertEqual(dobj._resolve_comment('a'), 'A')
        self.assertEqual(dobj._resolve_comment('b'), 'B')
        self.assertEqual(dobj._resolve_comment('c'), None)

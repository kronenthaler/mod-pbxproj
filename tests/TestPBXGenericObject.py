import unittest

from pbxproj import PBXGenericObject
from pbxproj.PBXObjects import objects
from pbxproj.PBXKey import PBXKey


class PBXGenericObjectTest(unittest.TestCase):
    def testParseCreateAttributes(self):
        obj = {"a": "varA", "b": [1, 2, 3], "c": {"c1": "varC1"}}
        dobj = PBXGenericObject().parse(obj)
        assert dobj.a == "varA"
        assert dobj.b == [1, 2, 3]
        assert dobj.c is not None

    def testParseCreateObjectOfRightTypes(self):
        obj = {"objects": {"id": {"isa": "type"}}}
        dobj = PBXGenericObject().parse(obj)

        assert isinstance(dobj.objects, objects)

    def testParseKey(self):
        obj = "FDDF6A571C68E5B100D7A645"
        dobj = PBXGenericObject().parse(obj)

        assert isinstance(dobj, PBXKey)

    def testEscapeItem(self):
        assert PBXGenericObject._escape("/bin/sh") == "/bin/sh"
        assert PBXGenericObject._escape("/bin/sh\n") == '"/bin/sh\\n"'
        assert PBXGenericObject._escape("abcdefghijklmnopqrstuvwyz0123456789") == \
                         "abcdefghijklmnopqrstuvwyz0123456789"
        assert PBXGenericObject._escape("some spaces") == '"some spaces"'
        assert PBXGenericObject._escape("a.valid_id.") == "a.valid_id."
        assert PBXGenericObject._escape("a-invalid-id") == '"a-invalid-id"'
        assert PBXGenericObject._escape("<group>") == '"<group>"'
        assert PBXGenericObject._escape("script \\ continuation") == '"script \\\\ continuation"'
        assert PBXGenericObject._escape("/bin/sh find .. -name '*.framework'", exclude=["\'"]) == \
                         "\"/bin/sh find .. -name '*.framework'\""

    def testPrintObject(self):
        obj = {"a": "varA", "b": [1, 2, 3], "c": {"c1": "FDDF6A571C68E5B100D7A645"}}
        dobj = PBXGenericObject().parse(obj)

        expected = '{\n\ta = varA;\n\tb = (\n\t\t1,\n\t\t2,\n\t\t3,\n\t);\n\tc = {\n\t\tc1 = FDDF6A571C68E5B100D7A645;\n\t};\n}'

        assert dobj.__repr__() == expected

    def testGetItem(self):
        obj = {"a": "varA", "b": [1, 2, 3], "c": {"c1": "FDDF6A571C68E5B100D7A645"}}
        dobj = PBXGenericObject().parse(obj)

        assert isinstance(dobj["c"]["c1"], PBXKey)
        assert dobj['X'] is None

    def testSetItemNone(self):
        obj = {}
        dobj = PBXGenericObject().parse(obj)

        assert dobj['something'] is None

        dobj['something'] = None
        assert dobj['something'] is None

    def testSetItemString(self):
        obj = {}
        dobj = PBXGenericObject().parse(obj)

        assert dobj['something'] is None

        dobj['something'] = 'yes'
        assert dobj['something'] == 'yes'

    def testSetItemListOfZero(self):
        obj = {}
        dobj = PBXGenericObject().parse(obj)

        assert dobj['something'] is None

        dobj['something'] = []
        assert dobj['something'] is None

    def testSetItemListOfOne(self):
        obj = {}
        dobj = PBXGenericObject().parse(obj)

        assert dobj['something'] is None

        dobj['something'] = ['yes']
        assert dobj['something'] == 'yes'

    def testSetItemListOfTwo(self):
        obj = {}
        dobj = PBXGenericObject().parse(obj)

        assert dobj['something'] is None

        dobj['something'] = ['yes', 'yes']
        assert dobj['something'] == ['yes', 'yes']

    def testResolveComment(self):
        obj = {"a": {"name": "A"}, "b": {"path": "B"}, "c": {"c1": "FDDF6A571C68E5B100D7A645"}}
        dobj = PBXGenericObject().parse(obj)

        assert dobj._resolve_comment('a') == 'A'
        assert dobj._resolve_comment('b') == 'B'
        assert dobj._resolve_comment('c') == None

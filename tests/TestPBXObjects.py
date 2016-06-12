import unittest

from pbxproj.PBXObjects import objects


class PBXObjectTest(unittest.TestCase):
    MINIMUM_OBJ = {'1': {'isa': 'phase1'}, '2': {'isa': 'phase1'}, '3': {'isa': 'phase2'}}

    def testParseNonObject(self):
        obj = [1, 2, 3]
        dobj = objects().parse(obj)

        self.assertIsInstance(dobj, list)

    def testParseGroupsPhases(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)

        self.assertEqual(dobj._sections.__len__(), 2)
        self.assertEqual(dobj._sections['phase1'].__len__(), 2)
        self.assertEqual(dobj._sections['phase2'].__len__(), 1)

    def testPrintSeparateSections(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        str = dobj.__repr__()

        self.assertTrue(str.__contains__("/* Begin phase1 section */"))
        self.assertTrue(str.__contains__("/* End phase1 section */"))
        self.assertTrue(str.__contains__("/* Begin phase2 section */"))
        self.assertTrue(str.__contains__("/* End phase2 section */"))

    def testGetItem(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        self.assertIsNotNone(dobj['1'])
        self.assertIsNone(dobj['4'])

    def testContains(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        self.assertTrue('1' in dobj)
        self.assertFalse('4' in dobj)

    def testIndexOf(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        item = dobj['1']
        self.assertEqual(dobj.indexOf(item), '1')
        self.assertEqual(dobj.indexOf(None), None)

    def testGetObjectsInsection(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        self.assertEqual(dobj.get_objects_in_section('phase1'), dobj._sections['phase1'])
        self.assertEqual(dobj.get_objects_in_section('phaseX'), [])
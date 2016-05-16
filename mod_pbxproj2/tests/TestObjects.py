import unittest
from mod_pbxproj2 import *


class ObjectTest(unittest.TestCase):
    MINIMUM_OBJ = {'1': {'isa': 'phase1'}, '2': {'isa': 'phase1'}, '3': {'isa': 'phase2'}}

    def testParseNonObject(self):
        obj = [1, 2, 3]
        dobj = objects().parse(obj)

        self.assertIsInstance(dobj, list)

    def testParseGroupsPhases(self):
        dobj = objects().parse(ObjectTest.MINIMUM_OBJ)

        self.assertEqual(dobj._sections.__len__(), 2)
        self.assertEqual(dobj._sections['phase1'].__len__(), 2)
        self.assertEqual(dobj._sections['phase2'].__len__(), 1)

    def testPrintSeparateSections(self):
        dobj = objects().parse(ObjectTest.MINIMUM_OBJ)
        str = dobj.__repr__()

        self.assertTrue(str.__contains__("/* Begin phase1 section */"))
        self.assertTrue(str.__contains__("/* End phase1 section */"))
        self.assertTrue(str.__contains__("/* Begin phase2 section */"))
        self.assertTrue(str.__contains__("/* End phase2 section */"))
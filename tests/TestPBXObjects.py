import unittest

from pbxproj.PBXObjects import objects


class PBXObjectTest(unittest.TestCase):
    MINIMUM_OBJ = {'3': {'isa': 'phase2'}, '1': {'isa': 'phase1'}, '2': {'isa': 'phase1'}}

    def testParseNonObject(self):
        obj = [1, 2, 3]
        dobj = objects().parse(obj)

        self.assertIsInstance(dobj, list)

    def testGetKeys(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        keys = dobj.get_keys()

        self.assertListEqual(keys, ['1', '2', '3'])

    def testParseGroupsPhases(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)

        self.assertEqual(dobj._sections.__len__(), 2)
        self.assertEqual(dobj._sections['phase1'].__len__(), 2)
        self.assertEqual(dobj._sections['phase2'].__len__(), 1)

    def testPrintSeparateSections(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        string = dobj.__repr__()

        self.assertTrue(string.__contains__('/* Begin phase1 section */'))
        self.assertTrue(string.__contains__('/* End phase1 section */'))
        self.assertTrue(string.__contains__('/* Begin phase2 section */'))
        self.assertTrue(string.__contains__('/* End phase2 section */'))

    def testGetItem(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        self.assertIsNotNone(dobj['1'])
        self.assertIsNone(dobj['4'])

    def testContains(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        self.assertTrue('1' in dobj)
        self.assertFalse('4' in dobj)

    def testGetObjectsInsection(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        sections = dobj.get_objects_in_section('phase1', 'phase2')

        self.assertSetEqual(set(sections).intersection(dobj._sections['phase1']), set(dobj._sections['phase1']))
        self.assertSetEqual(set(sections).intersection(dobj._sections['phase2']), set(dobj._sections['phase2']))
        self.assertEqual(dobj.get_objects_in_section('phaseX'), [])

    def testGetTargets(self):
        obj = {
            '1': {'isa': 'PBXNativeTarget', 'name': 'app'},
            '2': {'isa': 'PBXAggregateTarget', 'name': 'report'},
            '3': {'isa': 'PBXNativeTarget', 'name': 'something'}
        }
        dobj = objects().parse(obj)

        self.assertEqual(dobj.get_targets().__len__(), 3)
        self.assertEqual(dobj.get_targets('app').__len__(), 1)
        self.assertEqual(dobj.get_targets('report').__len__(), 1)
        self.assertEqual(dobj.get_targets('whatever').__len__(), 0)
        self.assertEqual(dobj.get_targets(['app', 'something']).__len__(), 2)

    def testGetConfigurationTargets(self):
        obj = {
            '1': {'isa': 'PBXNativeTarget', 'name': 'app', 'buildConfigurationList': '3'},
            '2': {'isa': 'PBXAggregateTarget', 'name': 'report', 'buildConfigurationList': '4'},
            '3': {'isa': 'XCConfigurationList', 'buildConfigurations': ['5', '6']},
            '4': {'isa': 'XCConfigurationList', 'buildConfigurations': ['7', '8']},
            '5': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'id': '5'},
            '6': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '6'},
            '7': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'id': '7'},
            '8': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '8'},
        }
        dobj = objects().parse(obj)

        result = [x for x in dobj.get_configurations_on_targets()]
        self.assertEqual(result.__len__(), 4)
        self.assertSetEqual({x.id for x in result}, {'5', '6', '7', '8'})

        result = [x for x in dobj.get_configurations_on_targets(target_name='app')]
        self.assertEqual(result.__len__(), 2)
        self.assertSetEqual({x.id for x in result}, {'5', '6'})

        result = [x for x in dobj.get_configurations_on_targets(configuration_name='Release')]
        self.assertSetEqual({x.id for x in result}, {'5', '7'})

        result = [x for x in dobj.get_configurations_on_targets(target_name='app', configuration_name='Release')]
        self.assertEqual(result.__len__(), 1)
        self.assertSetEqual({x.id for x in result}, {'5'})

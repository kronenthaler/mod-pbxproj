import unittest

from pbxproj.PBXObjects import objects


class PBXObjectTest(unittest.TestCase):
    MINIMUM_OBJ = {'3': {'isa': 'phase2'}, '1': {'isa': 'phase1'}, '2': {'isa': 'phase1'}}

    def testParseNonObject(self):
        obj = [1, 2, 3]
        dobj = objects().parse(obj)

        assert isinstance(dobj, list)

    def testGetKeys(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        keys = dobj.get_keys()

        assert keys == ['1', '2', '3']

    def testParseGroupsPhases(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)

        assert dobj._sections.__len__() == 2
        assert dobj._sections['phase1'].__len__() == 2
        assert dobj._sections['phase2'].__len__() == 1

    def testPrintSeparateSections(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        string = dobj.__repr__()

        assert string.__contains__('/* Begin phase1 section */')
        assert string.__contains__('/* End phase1 section */')
        assert string.__contains__('/* Begin phase2 section */')
        assert string.__contains__('/* End phase2 section */')

    def testGetItem(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        assert dobj['1'] is not None
        assert dobj['4'] is None

    def testContains(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        assert '1' in dobj
        assert not ('4' in dobj)

    def testGetObjectsInsection(self):
        dobj = objects().parse(PBXObjectTest.MINIMUM_OBJ)
        sections = dobj.get_objects_in_section('phase1', 'phase2')

        assert set(sections).intersection(dobj._sections['phase1']) == set(dobj._sections['phase1'])
        assert set(sections).intersection(dobj._sections['phase2']) == set(dobj._sections['phase2'])
        assert dobj.get_objects_in_section('phaseX') == []

    def testGetTargets(self):
        obj = {
            '1': {'isa': 'PBXNativeTarget', 'name': 'app'},
            '2': {'isa': 'PBXAggregateTarget', 'name': 'report'},
            '3': {'isa': 'PBXNativeTarget', 'name': 'something'}
        }
        dobj = objects().parse(obj)

        assert dobj.get_targets().__len__() == 3
        assert dobj.get_targets('app').__len__() == 1
        assert dobj.get_targets('report').__len__() == 1
        assert dobj.get_targets('whatever').__len__() == 0
        assert dobj.get_targets(['app', 'something']).__len__() == 2

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
        assert result.__len__() == 4
        assert {x.id for x in result} == {'5', '6', '7', '8'}

        result = [x for x in dobj.get_configurations_on_targets(target_name='app')]
        assert result.__len__() == 2
        assert {x.id for x in result} == {'5', '6'}

        result = [x for x in dobj.get_configurations_on_targets(configuration_name='Release')]
        assert {x.id for x in result} == {'5', '7'}

        result = [x for x in dobj.get_configurations_on_targets(target_name='app', configuration_name='Release')]
        assert result.__len__() == 1
        assert {x.id for x in result} == {'5'}

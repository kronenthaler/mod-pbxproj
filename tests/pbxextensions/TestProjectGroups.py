import unittest

from pbxproj import XcodeProject
from pbxproj.pbxextensions import ProjectGroups
import pytest


class ProjectGroupsTest(unittest.TestCase):
    def setUp(self):
        self.obj = {
            'objects': {
                'root': {'isa': 'PBXGroup', 'children': ['1', '1p']},
                '1': {'isa': 'PBXGroup', 'name': 'root', 'children': ['2', '3']},
                '2': {'isa': 'PBXGroup', 'name': 'app', 'children': []},
                '3': {'isa': 'PBXGroup', 'name': 'app', 'children': []},
                '4': {'isa': 'PBXGroup', 'name': 'root', 'children': ['5', '6']},
                '5': {'isa': 'PBXGroup', 'name': 'app', 'children': []},
                '6': {'isa': 'PBXGroup', 'name': 'app', 'children': []},
                '1p': {'isa': 'PBXGroup', 'name': 'root', 'children': ['2p', '3p']},
                '2p': {'isa': 'PBXGroup', 'name': 'app', 'path': '..', 'children': []},
                '3p': {'isa': 'PBXGroup', 'name': 'app', 'path': '..', 'children': []},
                '4p': {'isa': 'PBXGroup', 'name': 'root', 'children': ['5p', '6p']},
                '5p': {'isa': 'PBXGroup', 'name': 'app', 'path': '..', 'children': []},
                '6p': {'isa': 'PBXGroup', 'name': 'app', 'path': '..', 'children': []},
                'broken': {'isa': 'PBXGroup', 'name': 'broken', 'path': '..', 'children': ['broken1']},
                'broken1': {'isa': 'PBXGroup', 'name': 'b1', 'path': '..', 'children': ['broken2']},
                'a': {'isa': 'PBXGroup', 'name': 'app', 'path': '..', 'children': ['b']},
                'b': {'isa': 'PBXGroup', 'name': 'app', 'path': '..', 'children': ['c']},
                'c': {'isa': 'PBXFileReference', 'name': 'app'},
            },
        }

    def testInit(self):
        with pytest.raises(EnvironmentError, match='^This class cannot be instantiated directly'):
            ProjectGroups()

    def testGetGroupsByNameNoParent(self):
        project = XcodeProject(self.obj)
        groups = project.get_groups_by_name('app')

        assert project.objects['2'] in groups
        assert project.objects['3'] in groups
        assert project.objects['5'] in groups
        assert project.objects['6'] in groups

    def testGetGroupsByNameFromParent(self):
        project = XcodeProject(self.obj)
        groups = project.get_groups_by_name('app', parent=project.objects['1'])

        assert project.objects['2'] in groups
        assert project.objects['3'] in groups
        assert project.objects['5'] not in groups
        assert project.objects['6'] not in groups

    def testGetGroupsByPathNoParent(self):
        project = XcodeProject(self.obj)
        groups = project.get_groups_by_path('..')

        assert project.objects['2p'] in groups
        assert project.objects['3p'] in groups
        assert project.objects['5p'] in groups
        assert project.objects['6p'] in groups

    def testGetGroupsByPathFromParent(self):
        project = XcodeProject(self.obj)
        groups = project.get_groups_by_path('..', parent=project.objects['1p'])

        assert project.objects['2p'] in groups
        assert project.objects['3p'] in groups
        assert project.objects['5p'] not in groups
        assert project.objects['6p'] not in groups

    def testAddGroupNoParent(self):
        project = XcodeProject(self.obj)
        group = project.add_group('my_group')

        assert project.objects['root'].has_child(group)

    def testAddGroupToParent(self):
        project = XcodeProject(self.obj)
        group = project.add_group('my_group', parent=project.objects['1'])

        assert project.objects['1'].has_child(group)

    def testRemoveByIdNotFound(self):
        project = XcodeProject(self.obj)

        assert not project.remove_group_by_id('xxx')

    def testRemoveByIdRecursive(self):
        project = XcodeProject(self.obj)
        group1 = project.objects['1']
        result = project.remove_group_by_id('1', recursive=True)

        assert result
        assert not project.objects['root'].has_child(group1)
        assert project.objects['1'] is None
        assert project.objects['2'] is None
        assert project.objects['3'] is None

    def testRemoveByIdNonRecursive(self):
        project = XcodeProject(self.obj)
        group = project.objects['1']
        result = project.remove_group_by_id('1', recursive=False)

        assert result
        assert not project.objects['root'].has_child(group)
        assert project.objects['1'] is None
        assert project.objects['2'] is not None
        assert project.objects['3'] is not None

    def testRemoveByNameNotFound(self):
        project = XcodeProject(self.obj)

        assert not project.remove_group_by_name('xxx')

    def testRemoveByNameRecursive(self):
        project = XcodeProject(self.obj)
        group1 = project.objects['1']
        group1p = project.objects['1p']
        result = project.remove_group_by_name('root', recursive=True)

        assert result
        assert not project.objects['root'].has_child(group1)
        assert not project.objects['root'].has_child(group1p)
        assert project.objects['1'] is None
        assert project.objects['2'] is None
        assert project.objects['3'] is None
        assert project.objects['1p'] is None
        assert project.objects['2p'] is None
        assert project.objects['3p'] is None

    def testRemoveByNameNonRecursive(self):
        project = XcodeProject(self.obj)
        group1 = project.objects['1']
        group1p = project.objects['1p']
        result = project.remove_group_by_name('root', recursive=False)

        assert result
        assert not project.objects['root'].has_child(group1)
        assert not project.objects['root'].has_child(group1p)
        assert project.objects['1'] is None
        assert project.objects['2'] is not None
        assert project.objects['3'] is not None
        assert project.objects['1p'] is None
        assert project.objects['2p'] is not None
        assert project.objects['3p'] is not None

    def testRemoveByIdRecursivelyWithFiles(self):
        project = XcodeProject(self.obj)
        result = project.remove_group_by_id('a')

        assert result
        assert project.objects['a'] is None
        assert project.objects['b'] is None
        assert project.objects['c'] is None

    def testRemoveBrokenGroups(self):
        project = XcodeProject(self.obj)
        result = project.remove_group_by_id('broken')

        assert not result

    def testRemoveBrokenGroupsByName(self):
        project = XcodeProject(self.obj)
        result = project.remove_group_by_name('broken')

        assert not result

    def testGetOrCreateGroupNoName(self):
        project = XcodeProject(self.obj)
        group = project.get_or_create_group(None)

        assert group is None

    def testGetOrCreateGroupNotFound(self):
        project = XcodeProject(self.obj)
        group = project.get_or_create_group('whatever')

        assert group is not None
        assert group.get_id() not in self.obj['objects']

    def testGetOrCreateGroupFound(self):
        project = XcodeProject(self.obj)
        group = project.get_or_create_group('root')

        assert group is not None
        assert group.get_id() in self.obj['objects']

    def testGetParentGroupCreateDefault(self):
        project = XcodeProject({'objects': {}})
        group = project._get_parent_group(None)

        assert group is not None
        assert project.objects[group.get_id()] == group

    def testGetParentGroupFromMainGroup(self):
        project = XcodeProject(
            {
                'objects': {
                    'project': {'isa': 'PBXProject', 'mainGroup': 'group'},
                    'group': {'isa': 'PBXGroup', 'name': 'group1'}
                },
                'rootObject': 'project'
            })
        group = project._get_parent_group(None)

        assert group is not None
        assert project.objects[project.objects['project'].mainGroup] == group

    def testGetParentGroupWithID(self):
        project = XcodeProject(self.obj)
        parent = project._get_parent_group('5p')

        assert parent == project.objects['5p']

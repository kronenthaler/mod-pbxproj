import unittest

from pbxproj import XcodeProject
from pbxproj.pbxextensions import ProjectGroups


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
        with self.assertRaisesRegex(EnvironmentError, '^This class cannot be instantiated directly'):
            ProjectGroups()

    def testGetGroupsByNameNoParent(self):
        project = XcodeProject(self.obj)
        groups = project.get_groups_by_name('app')

        self.assertIn(project.objects['2'], groups)
        self.assertIn(project.objects['3'], groups)
        self.assertIn(project.objects['5'], groups)
        self.assertIn(project.objects['6'], groups)

    def testGetGroupsByNameFromParent(self):
        project = XcodeProject(self.obj)
        groups = project.get_groups_by_name('app', parent=project.objects['1'])

        self.assertIn(project.objects['2'], groups)
        self.assertIn(project.objects['3'], groups)
        self.assertNotIn(project.objects['5'], groups)
        self.assertNotIn(project.objects['6'], groups)

    def testGetGroupsByPathNoParent(self):
        project = XcodeProject(self.obj)
        groups = project.get_groups_by_path('..')

        self.assertIn(project.objects['2p'], groups)
        self.assertIn(project.objects['3p'], groups)
        self.assertIn(project.objects['5p'], groups)
        self.assertIn(project.objects['6p'], groups)

    def testGetGroupsByPathFromParent(self):
        project = XcodeProject(self.obj)
        groups = project.get_groups_by_path('..', parent=project.objects['1p'])

        self.assertIn(project.objects['2p'], groups)
        self.assertIn(project.objects['3p'], groups)
        self.assertNotIn(project.objects['5p'], groups)
        self.assertNotIn(project.objects['6p'], groups)

    def testAddGroupNoParent(self):
        project = XcodeProject(self.obj)
        group = project.add_group('my_group')

        self.assertTrue(project.objects['root'].has_child(group))

    def testAddGroupToParent(self):
        project = XcodeProject(self.obj)
        group = project.add_group('my_group', parent=project.objects['1'])

        self.assertTrue(project.objects['1'].has_child(group))

    def testRemoveByIdNotFound(self):
        project = XcodeProject(self.obj)

        self.assertFalse(project.remove_group_by_id('xxx'))

    def testRemoveByIdRecursive(self):
        project = XcodeProject(self.obj)
        group1 = project.objects['1']
        result = project.remove_group_by_id('1', recursive=True)

        self.assertTrue(result)
        self.assertFalse(project.objects['root'].has_child(group1))
        self.assertIsNone(project.objects['1'])
        self.assertIsNone(project.objects['2'])
        self.assertIsNone(project.objects['3'])

    def testRemoveByIdNonRecursive(self):
        project = XcodeProject(self.obj)
        group = project.objects['1']
        result = project.remove_group_by_id('1', recursive=False)

        self.assertTrue(result)
        self.assertFalse(project.objects['root'].has_child(group))
        self.assertIsNone(project.objects['1'])
        self.assertIsNotNone(project.objects['2'])
        self.assertIsNotNone(project.objects['3'])

    def testRemoveByNameNotFound(self):
        project = XcodeProject(self.obj)

        self.assertFalse(project.remove_group_by_name('xxx'))

    def testRemoveByNameRecursive(self):
        project = XcodeProject(self.obj)
        group1 = project.objects['1']
        group1p = project.objects['1p']
        result = project.remove_group_by_name('root', recursive=True)

        self.assertTrue(result)
        self.assertFalse(project.objects['root'].has_child(group1))
        self.assertFalse(project.objects['root'].has_child(group1p))
        self.assertIsNone(project.objects['1'])
        self.assertIsNone(project.objects['2'])
        self.assertIsNone(project.objects['3'])
        self.assertIsNone(project.objects['1p'])
        self.assertIsNone(project.objects['2p'])
        self.assertIsNone(project.objects['3p'])

    def testRemoveByNameNonRecursive(self):
        project = XcodeProject(self.obj)
        group1 = project.objects['1']
        group1p = project.objects['1p']
        result = project.remove_group_by_name('root', recursive=False)

        self.assertTrue(result)
        self.assertFalse(project.objects['root'].has_child(group1))
        self.assertFalse(project.objects['root'].has_child(group1p))
        self.assertIsNone(project.objects['1'])
        self.assertIsNotNone(project.objects['2'])
        self.assertIsNotNone(project.objects['3'])
        self.assertIsNone(project.objects['1p'])
        self.assertIsNotNone(project.objects['2p'])
        self.assertIsNotNone(project.objects['3p'])

    def testRemoveByIdRecursivelyWithFiles(self):
        project = XcodeProject(self.obj)
        result = project.remove_group_by_id('a')

        self.assertTrue(result)
        self.assertIsNone(project.objects['a'])
        self.assertIsNone(project.objects['b'])
        self.assertIsNone(project.objects['c'])

    def testRemoveBrokenGroups(self):
        project = XcodeProject(self.obj)
        result = project.remove_group_by_id('broken')

        self.assertFalse(result)

    def testRemoveBrokenGroupsByName(self):
        project = XcodeProject(self.obj)
        result = project.remove_group_by_name('broken')

        self.assertFalse(result)

    def testGetOrCreateGroupNoName(self):
        project = XcodeProject(self.obj)
        group = project.get_or_create_group(None)

        self.assertIsNone(group)

    def testGetOrCreateGroupNotFound(self):
        project = XcodeProject(self.obj)
        group = project.get_or_create_group('whatever')

        self.assertIsNotNone(group)
        self.assertNotIn(group.get_id(), self.obj['objects'])

    def testGetOrCreateGroupFound(self):
        project = XcodeProject(self.obj)
        group = project.get_or_create_group('root')

        self.assertIsNotNone(group)
        self.assertIn(group.get_id(), self.obj['objects'])

    def testGetParentGroupCreateDefault(self):
        project = XcodeProject({'objects': {}})
        group = project._get_parent_group(None)

        self.assertIsNotNone(group)
        self.assertEqual(project.objects[group.get_id()], group)

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

        self.assertIsNotNone(group)
        self.assertEqual(project.objects[project.objects['project'].mainGroup], group)

    def testGetParentGroupWithID(self):
        project = XcodeProject(self.obj)
        parent = project._get_parent_group('5p')

        self.assertEqual(parent, project.objects['5p'])

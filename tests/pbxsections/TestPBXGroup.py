import unittest
from pbxproj.pbxsections.PBXGroup import *


class PBXGroupTests(unittest.TestCase):
    def testCreateWithoutName(self):
        group = PBXGroup.create('folder_name')
        self.assertFalse(u'name' in group)
        self.assertEqual(group.path, 'folder_name')

    def testCreateWithName(self):
        group = PBXGroup.create('folder_name', 'Friendly Name')
        self.assertTrue(u'name' in group)
        self.assertEqual(group.path, 'folder_name')
        self.assertEqual(group.name, 'Friendly Name')

    def testGetNameWithoutName(self):
        group = PBXGroup.create('folder_name')
        self.assertEqual(group.get_name(), 'folder_name')

    def testGetNameWithName(self):
        group = PBXGroup.create('folder_name', 'Friendly Name')
        self.assertEqual(group.get_name(), 'Friendly Name')

    def testHasChild(self):
        group = PBXGroup.create('folder_name', children=['child1', 'child2'])
        self.assertTrue(group.has_child('child1'))
        self.assertTrue(group.has_child('child2'))
        self.assertFalse(group.has_child('child3'))

    def testHasChildIncomplete(self):
        group = PBXGroup().parse({'name': 'group'})
        self.assertFalse(group.has_child('child1'))

    def testAddInvalidChild(self):
        group = PBXGroup().parse({'name': 'group'})
        invalid_group = PBXGenericObject().parse({'_id': "not-a-group"})
        group.add_child(invalid_group)
        self.assertFalse(group.has_child(invalid_group))

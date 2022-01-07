import unittest

from pbxproj import PBXGenericObject
from pbxproj.PBXObjects import objects
from pbxproj.pbxextensions import TreeType
from pbxproj.pbxsections import PBXGroup


class PBXGroupTests(unittest.TestCase):
    def setUp(self):
        self.obj = {
            "z1": {"isa": "PBXGroup", "children": ["3a"], "path": "X", "sourceTree": TreeType.GROUP},
            "1": {"isa": "PBXGroup", "children": ["2", "3a"], "path": "X", "sourceTree": TreeType.GROUP},
            "2": {"isa": "PBXGroup", "children": ["4", "5a"], "path": "Y", "sourceTree": TreeType.GROUP},
            "3": {"isa": "PBXBuildFile", "fileRef": "3a"},
            "3a": {"isa": "PBXFileReference", "lastKnownFileType": "sourcecode.c.h", "name": "3a.h",
                   "path": "Source/3a.h", "sourceTree": "SOURCE_ROOT"},
            "4": {"isa": "PBXGroup", "children": ["6a"], "path": "Y", "sourceTree": TreeType.GROUP},
            "5": {"isa": "PBXBuildFile", "fileRef": "5a"},
            "5a": {"isa": "PBXFileReference", "lastKnownFileType": "sourcecode.c.h", "name": "5a.h",
                   "path": "Source/5a.h", "sourceTree": "SOURCE_ROOT"},
            "6": {"isa": "PBXBuildFile", "fileRef": "6a"},
            "6a": {"isa": "PBXFileReference", "lastKnownFileType": "sourcecode.c.h", "name": "6a.h",
                   "path": "Source/6a.h", "sourceTree": "SOURCE_ROOT"},
            "bp": {"isa": "PBXSourcesBuildPhase", "files": ["3", "5", "6"]},
            "ss": {"isa": "PBXShellScriptBuildPhase"}
        }

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

    def testRemoveGroupRecusively(self):
        objs = objects().parse(self.obj)
        objs["1"].remove()

        self.assertIsNone(objs["1"])
        self.assertIsNone(objs["2"])
        self.assertIsNone(objs["3"])
        self.assertIsNone(objs["3a"])
        self.assertIsNone(objs["4"])
        self.assertIsNone(objs["5"])
        self.assertIsNone(objs["5a"])
        self.assertIsNone(objs["6"])
        self.assertIsNone(objs["6a"])
        self.assertEqual(objs["bp"].files, [])
        self.assertEqual(objs["z1"].children, [])

    def testRemoveGroupNonRecusively(self):
        objs = objects().parse(self.obj)
        objs["1"].remove(recursive=False)

        self.assertIsNone(objs["1"])
        self.assertIsNotNone(objs["2"])
        self.assertIsNotNone(objs["3"])
        self.assertIsNotNone(objs["3a"])
        self.assertIsNotNone(objs["4"])
        self.assertIsNotNone(objs["5"])
        self.assertIsNotNone(objs["5a"])
        self.assertIsNotNone(objs["6"])
        self.assertIsNotNone(objs["6a"])
        self.assertNotEqual(objs["bp"].files, [])
        self.assertNotEqual(objs["z1"].children, [])

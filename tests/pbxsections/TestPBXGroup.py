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
        assert not (u'name' in group)
        assert group.path == 'folder_name'

    def testCreateWithName(self):
        group = PBXGroup.create('folder_name', 'Friendly Name')
        assert u'name' in group
        assert group.path == 'folder_name'
        assert group.name == 'Friendly Name'

    def testGetNameWithoutName(self):
        group = PBXGroup.create('folder_name')
        assert group.get_name() == 'folder_name'

    def testGetNameWithName(self):
        group = PBXGroup.create('folder_name', 'Friendly Name')
        assert group.get_name() == 'Friendly Name'

    def testHasChild(self):
        group = PBXGroup.create('folder_name', children=['child1', 'child2'])
        assert group.has_child('child1')
        assert group.has_child('child2')
        assert not group.has_child('child3')

    def testHasChildIncomplete(self):
        group = PBXGroup().parse({'name': 'group'})
        assert not group.has_child('child1')

    def testAddInvalidChild(self):
        group = PBXGroup().parse({'name': 'group'})
        invalid_group = PBXGenericObject().parse({'_id': "not-a-group"})
        group.add_child(invalid_group)
        assert not group.has_child(invalid_group)

    def testRemoveGroupRecusively(self):
        objs = objects().parse(self.obj)
        objs["1"].remove()

        assert objs["1"] is None
        assert objs["2"] is None
        assert objs["3"] is None
        assert objs["3a"] is None
        assert objs["4"] is None
        assert objs["5"] is None
        assert objs["5a"] is None
        assert objs["6"] is None
        assert objs["6a"] is None
        assert objs["bp"].files == []
        assert objs["z1"].children == []

    def testRemoveGroupNonRecusively(self):
        objs = objects().parse(self.obj)
        objs["1"].remove(recursive=False)

        assert objs["1"] is None
        assert objs["2"] is not None
        assert objs["3"] is not None
        assert objs["3a"] is not None
        assert objs["4"] is not None
        assert objs["5"] is not None
        assert objs["5a"] is not None
        assert objs["6"] is not None
        assert objs["6a"] is not None
        assert objs["bp"].files != []
        assert objs["z1"].children != []

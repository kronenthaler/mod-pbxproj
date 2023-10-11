import unittest

from pbxproj.pbxsections.XCBuildConfiguration import XCBuildConfiguration


class XCBuildConfigurationTest(unittest.TestCase):
    def testAddFlagOnNewObject(self):
        obj = XCBuildConfiguration()
        obj.add_flags('flag', '-flag')

        assert obj.buildSettings is not None
        assert obj.buildSettings.flag is not None
        assert obj.buildSettings.flag == '-flag'

    def testAddFlagsOnNewObject(self):
        obj = XCBuildConfiguration()
        obj.add_flags('flag', ['-flag', '-another-flag'])

        assert obj.buildSettings is not None
        assert obj.buildSettings.flag is not None
        assert obj.buildSettings.flag == ['-flag', '-another-flag']

    def testAddFlagOnSingleFlag(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': '-flag'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.add_flags('flag', '-another-flag')
        assert dobj.buildSettings.flag == ['-flag', '-another-flag']

    def testAddFlagOnMultipleFlags(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': ['-flag', '-b-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.add_flags('flag', '-another-flag')
        assert dobj.buildSettings.flag == ['-flag', '-b-flag', '-another-flag']

    def testAddFlagsOnSingleFlag(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': '-flag'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.add_flags('flag', ['-another-flag'])
        assert dobj.buildSettings.flag == ['-flag', '-another-flag']

    def testAddFlagsOnMultipleFlags(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': ['-flag', '-b-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.add_flags('flag', ['-another-flag'])
        assert dobj.buildSettings.flag == ['-flag', '-b-flag', '-another-flag']

    def testRemoveFlagOnEmpty(self):
        obj = {'isa': 'XCBuildConfiguration'}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.remove_flags('flag', '-flag')
        assert dobj['buildSettings'] is None

    def testRemoveFlagNonExistent(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag1': '-flag'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.remove_flags('flag', '-flag')
        assert dobj.buildSettings['flag'] is None

    def testRemoveFlagOnSingleValue(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': '-flag'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.remove_flags('flag', '-flag')
        assert dobj.buildSettings['flag'] is None

    def testRemoveFlagAllValues(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': '-flag'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.remove_flags('flag', None)
        assert dobj.buildSettings['flag'] is None

    def testRemoveFlagOnMultipleValue(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': ['-flag', '-b-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.remove_flags('flag', '-flag')
        assert dobj.buildSettings.flag == '-b-flag'

    def testAddSearchPathRecursiveUnEscaped(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.add_search_paths('search', '$(SRC_ROOT)', recursive=True)

        assert dobj.buildSettings.search == '$(SRC_ROOT)/**'

    def testAddSearchPathNonRecursiveUnEscaped(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.add_search_paths('search', '$(SRC_ROOT)', recursive=False)

        assert dobj.buildSettings.search == '$(SRC_ROOT)'

    def testAddSearchPathRecursiveEscaped(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.add_search_paths('search', '$(SRC_ROOT)', recursive=True, escape=True)

        assert dobj.buildSettings.search == '"$(SRC_ROOT)"/**'

    def testAddSearchPathNonRecursiveEscaped(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.add_search_paths('search', '$(SRC_ROOT)', recursive=False, escape=True)

        assert dobj.buildSettings.search == '"$(SRC_ROOT)"'

    def testAddSearchPathInherit(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.add_search_paths('search', '$(inherited)')

        assert dobj.buildSettings.search == '$(inherited)'

    def testRemoveSearchPath(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'search': '$(inherited)'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.remove_search_paths('search', '$(inherited)')

        assert dobj.buildSettings['search'] is None

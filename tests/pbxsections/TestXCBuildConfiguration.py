import unittest
from pbxproj.pbxsections.XCBuildConfiguration import *


class XCBuildConfigurationTest(unittest.TestCase):
    def testAddFlagOnNewObject(self):
        obj = XCBuildConfiguration()
        obj._add_flags('flag', '-flag')

        self.assertIsNotNone(obj.buildSettings)
        self.assertIsNotNone(obj.buildSettings.flag)
        self.assertEqual(obj.buildSettings.flag, '-flag')

    def testAddFlagsOnNewObject(self):
        obj = XCBuildConfiguration()
        obj._add_flags('flag', ['-flag', '-another-flag'])

        self.assertIsNotNone(obj.buildSettings)
        self.assertIsNotNone(obj.buildSettings.flag)
        self.assertListEqual(obj.buildSettings.flag, ['-flag', '-another-flag'])

    def testAddFlagOnSingleFlag(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': '-flag'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._add_flags('flag', '-another-flag')
        self.assertListEqual(dobj.buildSettings.flag, ['-flag', '-another-flag'])

    def testAddFlagOnMultipleFlags(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': ['-flag', '-b-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._add_flags('flag', '-another-flag')
        self.assertListEqual(dobj.buildSettings.flag, ['-flag', '-b-flag', '-another-flag'])

    def testAddFlagsOnSingleFlag(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': '-flag'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._add_flags('flag', ['-another-flag'])
        self.assertListEqual(dobj.buildSettings.flag, ['-flag', '-another-flag'])

    def testAddFlagsOnMultipleFlags(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': ['-flag', '-b-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._add_flags('flag', ['-another-flag'])
        self.assertListEqual(dobj.buildSettings.flag, ['-flag', '-b-flag', '-another-flag'])

    def testRemoveFlagOnEmpty(self):
        obj = {'isa': 'XCBuildConfiguration'}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._remove_flags('flag', '-flag')
        self.assertIsNone(dobj['buildSettings'])

    def testRemoveFlagNonExistent(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag1': '-flag'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._remove_flags('flag', '-flag')
        self.assertIsNone(dobj.buildSettings['flag'])

    def testRemoveFlagOnSingleValue(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': '-flag'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._remove_flags('flag','-flag')
        self.assertIsNone(dobj.buildSettings['flag'])

    def testRemoveFlagOnMultipleValue(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': ['-flag', '-b-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._remove_flags('flag', '-flag')
        self.assertEqual(dobj.buildSettings.flag, '-b-flag')

    def testAddOtherCFlags(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'OTHER_CFLAGS': ['-flag', '-b-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.add_other_cflags(['-another-flag'])
        self.assertListEqual(dobj.buildSettings.OTHER_CFLAGS, ['-flag', '-b-flag', '-another-flag'])

    def testAddOtherLDFlags(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'OTHER_LDFLAGS': ['-flag', '-b-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.add_other_ldflags(['-another-flag'])
        self.assertListEqual(dobj.buildSettings.OTHER_LDFLAGS, ['-flag', '-b-flag', '-another-flag'])

    def testRemoveOtherCFlags(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'OTHER_CFLAGS': ['-flag', '-b-flag', '-another-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.remove_other_cflags(['-flag'])
        self.assertListEqual(dobj.buildSettings.OTHER_CFLAGS, ['-b-flag', '-another-flag'])

    def testRemoveOtherLDFlags(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'OTHER_LDFLAGS': ['-flag', '-b-flag', '-another-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj.remove_other_ldflags(['-flag'])
        self.assertListEqual(dobj.buildSettings.OTHER_LDFLAGS, ['-b-flag', '-another-flag'])


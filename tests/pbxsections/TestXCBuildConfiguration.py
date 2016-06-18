import unittest
from pbxproj.pbxsections.XCBuildConfiguration import *


class XCBuildConfigurationTest(unittest.TestCase):
    def testAddFlagOnNewObject(self):
        obj = XCBuildConfiguration()
        obj._add_flag('flag', '-flag')

        self.assertIsNotNone(obj.buildSettings)
        self.assertIsNotNone(obj.buildSettings.flag)
        self.assertEqual(obj.buildSettings.flag, '-flag')

    def testAddFlagsOnNewObject(self):
        obj = XCBuildConfiguration()
        obj._add_flag('flag', ['-flag','-another-flag'])

        self.assertIsNotNone(obj.buildSettings)
        self.assertIsNotNone(obj.buildSettings.flag)
        self.assertListEqual(obj.buildSettings.flag, ['-flag', '-another-flag'])

    def testAddFlagOnSingleFlag(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': '-flag'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._add_flag('flag', '-another-flag')
        self.assertListEqual(dobj.buildSettings.flag, ['-flag', '-another-flag'])

    def testAddFlagOnMultipleFlags(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': ['-flag', '-b-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._add_flag('flag', '-another-flag')
        self.assertListEqual(dobj.buildSettings.flag, ['-flag', '-b-flag', '-another-flag'])

    def testAddFlagsOnSingleFlag(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': '-flag'}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._add_flag('flag', ['-another-flag'])
        self.assertListEqual(dobj.buildSettings.flag, ['-flag', '-another-flag'])

    def testAddFlagsOnMultipleFlags(self):
        obj = {'isa': 'XCBuildConfiguration', 'buildSettings': {'flag': ['-flag', '-b-flag']}}
        dobj = XCBuildConfiguration().parse(obj)

        dobj._add_flag('flag', ['-another-flag'])
        self.assertListEqual(dobj.buildSettings.flag, ['-flag', '-b-flag', '-another-flag'])

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

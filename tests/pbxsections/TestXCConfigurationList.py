import unittest
from pbxproj.pbxsections.XCConfigurationList import *
from pbxproj.PBXObjects import *


class XCConfigurationListTest(unittest.TestCase):
    def testGetComment(self):
        config = XCConfigurationList()
        config._get_section = lambda: ('TargetType', 'name')

        self.assertEqual(config._get_comment(), 'Build configuration list for TargetType "name"')

    def testGetSectionOnTarget(self):
        objs = objects(None).parse(
            {
                '1': {
                    'isa': 'PBXNativeTarget',
                    'buildConfigurationList': ['2'],
                    'name': 'the-target-name'
                },
                '2': {
                    'isa': 'XCConfigurationList'
                }
            })
        config = objs['2']
        self.assertEqual(config._get_comment(), 'Build configuration list for PBXNativeTarget "the-target-name"')

    def testGetSectionOnProject(self):
        objs = objects(None).parse(
            {
                "1": {
                    "isa": "PBXProject",
                    "buildConfigurationList": ['2'],
                    "targets": ["1"],
                    "productName": "the-target-name"
                },
                "2": {
                    'isa': 'XCConfigurationList'
                }
            })
        config = objs['2']
        self.assertEqual(config._get_comment(), 'Build configuration list for PBXProject "the-target-name"')

import unittest

from pbxproj import XCConfigurationList
from pbxproj.PBXObjects import objects


class XCConfigurationListTest(unittest.TestCase):
    def testGetComment(self):
        config = XCConfigurationList()
        config._get_section = lambda: ('TargetType', 'name')

        self.assertEqual(config._get_comment(), 'Build configuration list for TargetType "name"')

    def testGetSectionOnNativeTarget(self):
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

    def testGetSectionOnLegacyTarget(self):
        objs = objects(None).parse(
            {
                '1': {
                    'isa': 'PBXLegacyTarget',
                    'buildConfigurationList': ['2'],
                    'name': 'the-target-name'
                },
                '2': {
                    'isa': 'XCConfigurationList'
                }
            })
        config = objs['2']
        self.assertEqual(config._get_comment(), 'Build configuration list for PBXLegacyTarget "the-target-name"')

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

import unittest
from pbxproj.XcodeProject import *


class ProjectFlagsTest(unittest.TestCase):
    def setUp(self):
        self.obj = {
            'objects': {
                '1': {'isa': 'PBXNativeTarget', 'name': 'app', 'buildConfigurationList': '3'},
                '2': {'isa': 'PBXAggregatedTarget', 'name': 'report', 'buildConfigurationList': '4'},
                '3': {'isa': 'XCConfigurationList', 'buildConfigurations': ['5', '6']},
                '4': {'isa': 'XCConfigurationList', 'buildConfigurations': ['7', '8']},
                '5': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'buildSettings': {'base': 'a'} },
                '6': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '6'},
                '7': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'id': '7'},
                '8': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '8'},
            }
        }

    def testInit(self):
        with self.assertRaisesRegexp(EnvironmentError, '^This class cannot be instantiated directly'):
            ProjectFlags()

    def testAddFlags(self):
        project = XcodeProject(self.obj)
        project.add_flags('flag','-flag')

        self.assertEqual(project.objects['5'].buildSettings.flag, '-flag')
        self.assertEqual(project.objects['6'].buildSettings.flag, '-flag')
        self.assertEqual(project.objects['7'].buildSettings.flag, '-flag')
        self.assertEqual(project.objects['8'].buildSettings.flag, '-flag')

    def testRemoveFlags(self):
        project = XcodeProject(self.obj)
        project.remove_flags('base', 'a')

        self.assertIsNone(project.objects['5'].buildSettings['base'])

    def testAddOtherCFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_cflags('-ObjC')

        self.assertEqual(project.objects['5'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['6'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['7'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['8'].buildSettings.OTHER_CFLAGS, '-ObjC')

    def testAddOtherLDFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_ldflags('-ObjC')

        self.assertEqual(project.objects['5'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['6'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['7'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['8'].buildSettings.OTHER_LDFLAGS, '-ObjC')

    def testRemoveOtherCFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_cflags('-ObjC')
        self.assertEqual(project.objects['5'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['6'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['7'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['8'].buildSettings.OTHER_CFLAGS, '-ObjC')

        project.remove_other_cflags('-ObjC')

        self.assertIsNone(project.objects['5'].buildSettings['OTHER_CFLAGS'])
        self.assertIsNone(project.objects['6'].buildSettings['OTHER_CFLAGS'])
        self.assertIsNone(project.objects['7'].buildSettings['OTHER_CFLAGS'])
        self.assertIsNone(project.objects['8'].buildSettings['OTHER_CFLAGS'])


    def testRemoveOtherLDFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_ldflags('-ObjC')
        self.assertEqual(project.objects['5'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['6'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['7'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['8'].buildSettings.OTHER_LDFLAGS, '-ObjC')

        project.remove_other_ldflags('-ObjC')

        self.assertIsNone(project.objects['5'].buildSettings['OTHER_LDFLAGS'])
        self.assertIsNone(project.objects['6'].buildSettings['OTHER_LDFLAGS'])
        self.assertIsNone(project.objects['7'].buildSettings['OTHER_LDFLAGS'])
        self.assertIsNone(project.objects['8'].buildSettings['OTHER_LDFLAGS'])
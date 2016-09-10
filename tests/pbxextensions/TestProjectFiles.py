import unittest
from pbxproj.XcodeProject import *


class ProjectFilesTest(unittest.TestCase):
    def setUp(self):
        self.obj = {
            'objects': {
                '0': {'isa': 'PBXGroup', 'children': [], 'sourceTree': "<group>"},
                '1': {'isa': 'PBXNativeTarget', 'name': 'app', 'buildConfigurationList': '3', 'buildPhases': ['compile']},
                '2': {'isa': 'PBXAggregatedTarget', 'name': 'report', 'buildConfigurationList': '4', 'buildPhases': ['compile']},
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
            ProjectFiles()

    def testAddFileUnknown(self):
        project = XcodeProject(self.obj)
        with self.assertRaisesRegexp(ValueError, '^Unknown file extension: '):
            project.add_file("file.unknowntype")

    def testAddFileUnknownAllowed(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file("file.unknowntype", ignore_unknown_type=True)

        # unknown files are added as resources
        self.assertEqual(project.objects.get_objects_in_section(u'PBXResourcesBuildPhase').__len__(), 2)
        self.assertEqual(build_file.__len__(), 2)

    def testAddFileNoPath(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file(".", tree=None)

        # no tree or no path cannot be added
        self.assertEqual(build_file, [])

    def testAddFileNoCreateBuildFiles(self):
        project = XcodeProject(self.obj)
        items = project.objects.__len__()
        build_file = project.add_file(".", options=~BuildOptions.CREATE_BUILD_FILE_FLAG)

        # no create build file flag
        self.assertGreater(project.objects.__len__(), items)
        self.assertEqual(build_file, [])

    def testAddFileSource(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file("file.m")

        # 2 source files are created 1 x target
        self.assertEqual(project.objects.get_objects_in_section(u'PBXSourcesBuildPhase').__len__(), 2)
        self.assertEqual(build_file.__len__(), 2)

    def testAddFileFrameworkEmbedded(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file("file.framework", options=BuildOptions.WEAK_LINK_FLAG|BuildOptions.CREATE_BUILD_FILE_FLAG|BuildOptions.EMBED_FRAMEWORK)

        # 2 source files are created 1 x target
        self.assertEqual(project.objects.get_objects_in_section(u'PBXFrameworksBuildPhase').__len__(), 2)
        self.assertEqual(project.objects.get_objects_in_section(u'PBXCopyFilesBuildPhase').__len__(), 2)
        self.assertEqual(build_file.__len__(), 4)
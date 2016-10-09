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
        build_file = project.add_file(".", create_build_files=False)

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
        build_file = project.add_file("file.framework", create_build_files=True, weak=True, embed_framework=True)

        # 2 source files are created 1 x target
        self.assertEqual(project.objects.get_objects_in_section(u'PBXFrameworksBuildPhase').__len__(), 2)
        self.assertEqual(project.objects.get_objects_in_section(u'PBXCopyFilesBuildPhase').__len__(), 2)
        self.assertEqual(build_file.__len__(), 4)

    def testAddFileFrameworkWithAbsolutePath(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file(os.path.abspath("samples/test.framework"))

        expected_flags = ["$(SRCROOT)/tests/samples", "$(inherited)"]
        self.assertListEqual(project.objects['5'].buildSettings.FRAMEWORK_SEARCH_PATHS, expected_flags)
        self.assertListEqual(project.objects['6'].buildSettings.FRAMEWORK_SEARCH_PATHS, expected_flags)
        self.assertListEqual(project.objects['7'].buildSettings.FRAMEWORK_SEARCH_PATHS, expected_flags)
        self.assertListEqual(project.objects['8'].buildSettings.FRAMEWORK_SEARCH_PATHS, expected_flags)

    def testAddFileLibraryWithAbsolutePath(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file(os.path.abspath("samples/testLibrary.a"))

        expected_flags = "$(SRCROOT)/tests/samples"
        self.assertEqual(project.objects['5'].buildSettings.LIBRARY_SEARCH_PATHS, expected_flags)
        self.assertEqual(project.objects['6'].buildSettings.LIBRARY_SEARCH_PATHS, expected_flags)
        self.assertEqual(project.objects['7'].buildSettings.LIBRARY_SEARCH_PATHS, expected_flags)
        self.assertEqual(project.objects['8'].buildSettings.LIBRARY_SEARCH_PATHS, expected_flags)

    def testAddFileWithAbsolutePathDoesNotExist(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file(os.path.abspath("samples/unexistingFile.m"))

        # nothing to do if the file is absolute but doesn't exist
        self.assertListEqual(build_file, [])

    def testAddFileWithAbsolutePathOnUnknownTree(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file(os.path.abspath("samples/test.framework"), tree='DEVELOPER_DIR')

        self.assertEqual(project.objects[build_file[0].fileRef].sourceTree, '<absolute>')
        self.assertEqual(project.objects[build_file[1].fileRef].sourceTree, '<absolute>')
        self.assertEqual(project.objects[build_file[2].fileRef].sourceTree, '<absolute>')
        self.assertEqual(project.objects[build_file[3].fileRef].sourceTree, '<absolute>')

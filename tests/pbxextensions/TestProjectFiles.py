import os
import shutil
import unittest

from pbxproj import XcodeProject
from pbxproj.pbxextensions import ProjectFiles, FileOptions, TreeType, HeaderScope
from pbxproj.pbxsections import XCRemoteSwiftPackageReference, XCSwiftPackageProductDependency
import pytest

class ProjectFilesTest(unittest.TestCase):
    def setUp(self):
        self.obj = {
            'objects': {
                '0': {'isa': 'PBXGroup', 'children': ['group1'], 'sourceTree': "<group>"},
                '1': {'isa': 'PBXNativeTarget', 'name': 'app', 'buildConfigurationList': '3',
                      'buildPhases': ['compile1']},
                '2': {'isa': 'PBXAggregateTarget', 'name': 'report', 'buildConfigurationList': '4',
                      'buildPhases': ['compile']},
                '3': {'isa': 'XCConfigurationList', 'buildConfigurations': ['5', '6']},
                '4': {'isa': 'XCConfigurationList', 'buildConfigurations': ['7', '8']},
                '5': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'buildSettings': {'base': 'a'}},
                '6': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '6'},
                '7': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'id': '7'},
                '8': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '8'},
                # groups
                'group1': {'isa': 'PBXGroup', 'name': 'root', 'children': ['group2', 'group3']},
                'group2': {'isa': 'PBXGroup', 'name': 'app', 'children': ['file1', 'file2']},
                'group3': {'isa': 'PBXGroup', 'name': 'app', 'children': ['file3', 'group4', 'file4']},
                'group4': {'isa': 'PBXGroup', 'name': 'app', 'children': []},
                'file1': {'isa': 'PBXFileReference', 'name': 'file', 'path': 'file', 'sourceTree': 'SOURCE_ROOT'},
                'file2': {'isa': 'PBXFileReference', 'name': 'file', 'path': 'file', 'sourceTree': 'SOURCE_ROOT'},
                'file3': {'isa': 'PBXFileReference', 'name': 'file', 'path': 'file', 'sourceTree': 'SDKROOT'},
                'file4': {'isa': 'PBXFileReference', 'name': 'file1', 'path': 'file1', 'sourceTree': 'SOURCE_ROOT'},
                'file5': {'isa': 'PBXFileReference', 'path': 'file1', 'sourceTree': 'SOURCE_ROOT'},
                'build_file1': {'isa': 'PBXBuildFile', 'fileRef': 'file1'},
                'build_file2': {'isa': 'PBXBuildFile', 'fileRef': 'file2'},
                'compile': {'isa': 'PBXGenericBuildPhase', 'files': ['build_file1']},
                'compile1': {'isa': 'PBXCopyFilesBuildPhase', 'files': ['build_file2']},
                'compile2': {'isa': 'PBXShellScriptBuildPhase', 'files': []},
                'project': {'isa': 'PBXProject'}
            }
        }

        self.pwd = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

    def tearDown(self):
        os.chdir(self.pwd)

    def testInit(self):
        with pytest.raises(EnvironmentError, match='^This class cannot be instantiated directly'):
            ProjectFiles()

    def testAddFileUnknown(self):
        project = XcodeProject(self.obj)
        with pytest.raises(ValueError, match='^Unknown file extension: '):
            project.add_file("file.unknowntype")

    def testAddFileUnknownAllowed(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file("file.unknowntype", file_options=FileOptions(ignore_unknown_type=True))

        # unknown files are added as resources
        assert project.objects.get_objects_in_section(u'PBXResourcesBuildPhase').__len__() == 2
        assert build_file.__len__() == 2

    def testAddFileNoPath(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file(".", tree=None)

        # no tree or no path cannot be added
        assert build_file is None

    def testAddFileNoCreateBuildFiles(self):
        project = XcodeProject(self.obj)
        items = project.objects.__len__()
        build_file = project.add_file(".", file_options=FileOptions(create_build_files=False))

        # no create build file flag
        assert project.objects.__len__() == items
        assert build_file == []

    def testAddFileSource(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file("file.m")

        # 2 source files are created 1 x target
        assert project.objects.get_objects_in_section(u'PBXSourcesBuildPhase').__len__() == 2
        assert build_file.__len__() == 2

    def testAddFileXCFrameworkEmbedded(self):
        project = XcodeProject(self.obj)
        options = FileOptions(create_build_files=True, weak=True, embed_framework=True, code_sign_on_copy=True)
        build_file = project.add_file("samples/external.xcframework", file_options=options)

        # 2 source files are created 1 x target
        assert project.objects.get_objects_in_section(u'PBXFrameworksBuildPhase').__len__() == 2
        assert project.objects.get_objects_in_section(u'PBXCopyFilesBuildPhase').__len__() == 3
        assert build_file.__len__() == 4
        assert build_file[0].settings.ATTRIBUTES == [u'Weak']
        assert build_file[1].settings.ATTRIBUTES == [u'CodeSignOnCopy', u'RemoveHeadersOnCopy']
        assert build_file[2].settings.ATTRIBUTES == [u'Weak']
        assert build_file[3].settings.ATTRIBUTES == [u'CodeSignOnCopy', u'RemoveHeadersOnCopy']

    def testAddFileFrameworkEmbedded(self):
        project = XcodeProject(self.obj)
        options = FileOptions(create_build_files=True, weak=True, embed_framework=True, code_sign_on_copy=True)
        build_file = project.add_file("file.framework", file_options=options)

        # 2 source files are created 1 x target
        assert project.objects.get_objects_in_section(u'PBXFrameworksBuildPhase').__len__() == 2
        assert project.objects.get_objects_in_section(u'PBXCopyFilesBuildPhase').__len__() == 3
        assert build_file.__len__() == 4
        assert build_file[0].settings.ATTRIBUTES == [u'Weak']
        assert build_file[1].settings.ATTRIBUTES == [u'CodeSignOnCopy', u'RemoveHeadersOnCopy']
        assert build_file[2].settings.ATTRIBUTES == [u'Weak']
        assert build_file[3].settings.ATTRIBUTES == [u'CodeSignOnCopy', u'RemoveHeadersOnCopy']

    def testAddFileFrameworkFromSDKRootIgnoresEmbedAndCodeSign(self):
        project = XcodeProject(self.obj)
        options = FileOptions(create_build_files=True, weak=True, embed_framework=True, code_sign_on_copy=True)
        build_file = project.add_file("file.framework", tree=TreeType.SDKROOT, file_options=options)

        # 2 source files are created 1 x target
        assert project.objects.get_objects_in_section(u'PBXFrameworksBuildPhase').__len__() == 2
        assert project.objects.get_objects_in_section(u'PBXCopyFilesBuildPhase').__len__() == 3
        assert build_file.__len__() == 4
        assert build_file[0].settings.ATTRIBUTES == [u'Weak']
        assert build_file[1]['settings'] is None
        assert build_file[2].settings.ATTRIBUTES == [u'Weak']
        assert build_file[3]['settings'] is None

    def testAddFileFrameworkWithAbsolutePath(self):
        project = XcodeProject(self.obj)
        project.add_file(os.path.abspath("samples/test with spaces.framework"))

        expected_flags = ["$(SRCROOT)/tests/samples", "$(inherited)"]
        assert project.objects['5'].buildSettings.FRAMEWORK_SEARCH_PATHS == expected_flags
        assert project.objects['6'].buildSettings.FRAMEWORK_SEARCH_PATHS == expected_flags
        assert project.objects['7'].buildSettings.FRAMEWORK_SEARCH_PATHS == expected_flags
        assert project.objects['8'].buildSettings.FRAMEWORK_SEARCH_PATHS == expected_flags

    def testAddFileLibraryWithAbsolutePath(self):
        project = XcodeProject(self.obj)
        project.add_file(os.path.abspath("samples/path with spaces/testLibrary.a"))

        expected_flags = "\"$(SRCROOT)/tests/samples/path with spaces\""
        assert project.objects['5'].buildSettings.LIBRARY_SEARCH_PATHS == expected_flags
        assert project.objects['6'].buildSettings.LIBRARY_SEARCH_PATHS == expected_flags
        assert project.objects['7'].buildSettings.LIBRARY_SEARCH_PATHS == expected_flags
        assert project.objects['8'].buildSettings.LIBRARY_SEARCH_PATHS == expected_flags

    def testAddFileWithAbsolutePathDoesNotExist(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file(os.path.abspath("samples/unexistingFile.m"))

        # nothing to do if the file is absolute but doesn't exist
        assert build_file is None

    def testAddFileWithAbsolutePathOnUnknownTree(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file(os.path.abspath("samples/test with spaces.framework"), tree='DEVELOPER_DIR')

        assert project.objects[build_file[0].fileRef].sourceTree == TreeType.ABSOLUTE
        assert project.objects[build_file[1].fileRef].sourceTree == TreeType.ABSOLUTE
        assert project.objects[build_file[2].fileRef].sourceTree == TreeType.ABSOLUTE
        assert project.objects[build_file[3].fileRef].sourceTree == TreeType.ABSOLUTE

    def testAddReferenceFile(self):
        project = XcodeProject(self.obj, path="tests/project.pbxproj")
        build_file = project.add_file(os.path.abspath("samples/dirA"))

        assert project.objects.get_objects_in_section(u'PBXResourcesBuildPhase').__len__() == 2
        assert build_file.__len__() == 2

    def testAddFileIfExists(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file("file.m", force=False)

        # 2 source files are created 1 x target
        assert project.objects.get_objects_in_section(u'PBXSourcesBuildPhase').__len__() == 2
        assert build_file.__len__() == 2

        build_file = project.add_file("file.m", force=False)
        assert build_file == []

    def testAddFileIfExistsToMissingTargets(self):
        project = XcodeProject(self.obj)
        build_file = project.add_file("file.m", target_name='app', force=False)

        # 1 source files are created 1 x target
        assert project.objects.get_objects_in_section(u'PBXSourcesBuildPhase').__len__() == 1
        assert build_file.__len__() == 1

        build_file = project.add_file("file.m", force=False)
        assert project.objects.get_objects_in_section(u'PBXSourcesBuildPhase').__len__() == 2
        assert build_file.__len__() == 1

    def testAddFileOfAllTypes(self):
        for ext in ProjectFiles._FILE_TYPES:
            project = XcodeProject(self.obj)
            options = FileOptions(embed_framework=False)
            build_file = project.add_file("file{0}".format(ext), file_options=options)

            _, phase = ProjectFiles._FILE_TYPES[ext]
            amount = 0
            if phase is not None:
                amount = 2

            assert project.objects.get_objects_in_section(phase).__len__() == amount
            assert build_file.__len__() == amount

    def testGetFilesByNameWithNoParent(self):
        project = XcodeProject(self.obj)
        files = project.get_files_by_name('file')

        assert files.__len__() == 3

    def testGetFilesByNameWithParent(self):
        project = XcodeProject(self.obj)

        files = project.get_files_by_name('file', 'group2')
        assert files.__len__() == 2

        files = project.get_files_by_name('file', 'group3')
        assert files.__len__() == 1

    def testGetFilesByNameWithoutName(self):
        project = XcodeProject(self.obj)
        files = project.get_files_by_name('file1')

        assert files.__len__() == 2

    def testGetFileByPathWithNoTree(self):
        project = XcodeProject(self.obj)

        files = project.get_files_by_path('file')
        assert files.__len__() == 2

    def testGetFileByPathWithTree(self):
        project = XcodeProject(self.obj)

        files = project.get_files_by_path('file', TreeType.SDKROOT)
        assert files.__len__() == 1

    def testRemoveFileById(self):
        project = XcodeProject(self.obj)
        original = project.__str__()
        project.add_file("file.m")

        file = project.get_files_by_name('file.m')[0]
        result = project.remove_file_by_id(file.get_id())

        assert result
        assert project.__str__() == original

    def testRemoveFileByIdKeepShellScriptBuildPhases(self):
        project = XcodeProject(self.obj)
        project.add_run_script('ls -la')

        original = project.__str__()
        project.add_file("file.m")

        file = project.get_files_by_name('file.m')[0]
        result = project.remove_file_by_id(file.get_id())

        assert result
        assert project.__str__() == original

    def testRemoveFileByIdFromTarget(self):
        project = XcodeProject(self.obj)
        project.add_file("file.m")

        file_ref = project.get_files_by_name('file.m')[0]
        result = project.remove_file_by_id(file_ref.get_id(), target_name='report')

        assert result
        assert project.objects[file_ref.get_id()] is not None
        assert project.objects.get_objects_in_section('PBXBuildFile').__len__() == 3
        assert project.objects.get_objects_in_section('PBXSourcesBuildPhase').__len__() == 1

    def testRemoveFileByIdOnlyFiles(self):
        project = XcodeProject(self.obj)
        result = project.remove_file_by_id('group1')

        assert not result

    def testRemoveFilesByPath(self):
        project = XcodeProject(self.obj)
        original = project.__str__()
        project.add_file("file.m")

        result = project.remove_files_by_path('file.m')

        assert result
        assert project.__str__() == original

    def testAddFolderNotAFolder(self):
        project = XcodeProject(self.obj)
        result = project.add_folder('samples/testLibrary.a')

        assert result is None

    def testAddFolderNonRecursive(self):
        project = XcodeProject(self.obj)
        project.add_folder('samples/', recursive=False)

        # should add test with spaces.framework and testLibrary.a and 2 groups, samples, dirA
        samples = project.get_groups_by_name('samples')
        dir_a = project.get_groups_by_name('dirA')
        dir_b = project.get_groups_by_name('dirB')
        assert samples != []
        assert dir_a != []
        assert dir_b == []

        assert samples[0].children.__len__() == 4 # dirA, external.xcframework, test with spaces.framework, testLibrary.a
        assert dir_a[0].children.__len__() == 0

    def testAddFolderRecursive(self):
        project = XcodeProject(self.obj)
        project.add_folder('samples')

        # should add test with spaces.framework and testLibrary.a and 2 groups, samples, dirA
        samples = project.get_groups_by_name('samples')
        dir_a = project.get_groups_by_name('dirA')
        dir_b = project.get_groups_by_name('dirB')
        assert samples != []
        assert dir_a != []
        assert dir_b != []

        assert samples[0].children.__len__() == 4 # dirA, external.xcframework, test with spaces.framework, testLibrary.a
        assert dir_a[0].children.__len__() == 2  # dirB, fileA.m
        assert dir_b[0].children.__len__() == 2  # fileB.m, fileB.h

    def testAddFolderWithExclusions(self):
        project = XcodeProject(self.obj)
        project.add_folder('samples', excludes=['file.\\.m', 'test.*'])

        # should add test with spaces.framework and testLibrary.a and 2 groups, samples, dirA
        samples = project.get_groups_by_name('samples')
        dir_a = project.get_groups_by_name('dirA')
        dir_b = project.get_groups_by_name('dirB')
        assert samples != []
        assert dir_a != []
        assert dir_b != []

        assert samples[0].children.__len__() == 3  # dirA, external.xcframework, test with spaces.framework, -testLibrary.a
        assert dir_a[0].children.__len__() == 1  # dirB, -fileA.m
        assert dir_b[0].children.__len__() == 1  # -fileB.m, +fileB.h

    def testAddFolderAsReference(self):
        project = XcodeProject(self.obj, path="tests/project.pbxproj")
        build_file = project.add_folder('samples', create_groups=False)

        assert project.get_groups_by_name('samples') == []
        assert project.objects.get_objects_in_section(u'PBXResourcesBuildPhase').__len__() == 2
        assert build_file.__len__() == 2

    def testAddFolderWithPathSameAsName(self):
        project = XcodeProject(self.obj, path="tests/project.pbxproj")
        parent_group = project.get_or_create_group('parent_group')

        # Copy the samples folder into a folder to be added to the project.
        shutil.copytree('samples', 'parent_group/samples')

        target_path = 'parent_group/samples'
        project.add_folder(parent=parent_group, path=target_path, file_options=FileOptions(add_groups_relative=False))

        assert project.get_or_create_group('samples').path == os.path.abspath(target_path)

        shutil.rmtree('parent_group')

    def testEmbedFrameworkInRightCopySection(self):
        project = XcodeProject(self.obj)
        assert project.objects.get_objects_in_section(u'PBXCopyFilesBuildPhase').__len__() == 1

        project.add_file('X.framework', file_options=FileOptions(embed_framework=True))

        assert project.objects.get_objects_in_section(u'PBXCopyFilesBuildPhase').__len__() == 3

    def testAddProjectWithBuildPhases(self):
        project = XcodeProject(self.obj)

        frameworks = project.objects.get_objects_in_section('PBXFrameworksBuildPhase').__len__()
        resources = project.objects.get_objects_in_section('PBXResourcesBuildPhase').__len__()
        build_files = project.objects.get_objects_in_section('PBXBuildFile').__len__()

        reference_proxies = project.add_project('samplescli/dependency.xcodeproj')

        assert reference_proxies.__len__() == 2
        assert project.objects.get_objects_in_section(u'PBXContainerItemProxy').__len__() == 2
        assert project.objects.get_objects_in_section(u'PBXReferenceProxy').__len__() == 2
        assert project.objects.get_objects_in_section(u'PBXProject')[0].projectReferences.__len__() == 1

        # check that the buildFiles where added
        assert project.objects.get_objects_in_section('PBXBuildFile').__len__() > build_files
        assert project.objects.get_objects_in_section('PBXFrameworksBuildPhase').__len__() > frameworks
        assert project.objects.get_objects_in_section('PBXResourcesBuildPhase').__len__() > resources

    def testAddProjectWithoutBuildPhases(self):
        project = XcodeProject(self.obj)

        frameworks = project.objects.get_objects_in_section('PBXFrameworksBuildPhase').__len__()
        resources = project.objects.get_objects_in_section('PBXResourcesBuildPhase').__len__()
        build_files = project.objects.get_objects_in_section('PBXBuildFile').__len__()

        reference_proxies = project.add_project('samplescli/dependency.xcodeproj', file_options=FileOptions(create_build_files=False))

        assert reference_proxies.__len__() == 2
        assert project.objects.get_objects_in_section(u'PBXContainerItemProxy').__len__() == 2
        assert project.objects.get_objects_in_section(u'PBXReferenceProxy').__len__() == 2
        assert project.objects.get_objects_in_section(u'PBXProject')[0].projectReferences.__len__() == 1

        # check that the buildFiles where added
        assert project.objects.get_objects_in_section('PBXBuildFile').__len__() == build_files
        assert project.objects.get_objects_in_section('PBXFrameworksBuildPhase').__len__() == frameworks
        assert project.objects.get_objects_in_section('PBXResourcesBuildPhase').__len__() == resources

    def testAddProjectNotForced(self):
        project = XcodeProject(self.obj)

        _ = project.add_project('samplescli/dependency.xcodeproj', file_options=FileOptions(create_build_files=False))
        reference_proxies = project.add_project('samplescli/dependency.xcodeproj', force=False,
                                                file_options=FileOptions(create_build_files=False))

        assert reference_proxies == []

    def testAddProjectDoesntExists(self):
        project = XcodeProject(self.obj)
        reference_proxies = project.add_project(os.path.abspath("samples/unexistingFile.m"))

        # nothing to do if the file is absolute but doesn't exist
        assert reference_proxies is None

    def testAddHeaderFilePublic(self):
        project = XcodeProject({
            'objects': {
                '2': {'isa': 'PBXAggregateTarget', 'name': 'report', 'buildConfigurationList': '4',
                      'buildPhases': []},
                '4': {'isa': 'XCConfigurationList', 'buildConfigurations': ['7', '8']},
                '7': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'id': '7'},
                '8': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '8'},
                'project': {'isa': 'PBXProject'}
            }
        })

        assert project.get_build_phases_by_name(u'PBXHeadersBuildPhase').__len__() == 0

        references = project.add_file("header.h", file_options=FileOptions(header_scope=HeaderScope.PUBLIC))

        assert project.get_build_phases_by_name(u'PBXHeadersBuildPhase').__len__() > 0
        assert references[0].settings.ATTRIBUTES == ['Public']


    def testAddHeaderFilePrivate(self):
        project = XcodeProject({
            'objects': {
                '2': {'isa': 'PBXAggregateTarget', 'name': 'report', 'buildConfigurationList': '4',
                      'buildPhases': []},
                '4': {'isa': 'XCConfigurationList', 'buildConfigurations': ['7', '8']},
                '7': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'id': '7'},
                '8': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '8'},
                'project': {'isa': 'PBXProject'}
            }
        })

        assert project.get_build_phases_by_name(u'PBXHeadersBuildPhase').__len__() == 0

        references = project.add_file("header.h", file_options=FileOptions(header_scope=HeaderScope.PRIVATE))

        assert project.get_build_phases_by_name(u'PBXHeadersBuildPhase').__len__() > 0
        assert references[0].settings.ATTRIBUTES == ['Private']

    def testAddHeaderFileProjectScope(self):
        project = XcodeProject({
            'objects': {
                '2': {'isa': 'PBXAggregateTarget', 'name': 'report', 'buildConfigurationList': '4',
                      'buildPhases': []},
                '4': {'isa': 'XCConfigurationList', 'buildConfigurations': ['7', '8']},
                '7': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'id': '7'},
                '8': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '8'},
                'project': {'isa': 'PBXProject'}
            }
        })

        assert project.get_build_phases_by_name(u'PBXHeadersBuildPhase').__len__() == 0

        references = project.add_file("header.h", file_options=FileOptions())

        assert project.get_build_phases_by_name(u'PBXHeadersBuildPhase').__len__() > 0
        assert references[0]['settings'] is None, None

    def testAddPackage(self):
        project = XcodeProject({
            'objects': {
                '0': {'isa': 'PBXNativeTarget', 'name': 'app', 'buildPhases': []},
                'project': {'isa': 'PBXProject'}
            }
        })
        results = project.add_package('http://myrepo.com/some-package', { 
            "kind": "upToNextMajorVersion",
            "minimumVersion": "5.0.1"}, 'some-package', 'app')

        # create swift package reference and its entry into PBXProject package references
        assert isinstance(results[0], XCRemoteSwiftPackageReference)
        assert project.objects.get_objects_in_section('PBXProject')[0].packageReferences.__len__() == 1
        # create package product dependency and its entry into PBXNativeTarget package product depedency, 
        # PBXBuildFile and PBXFrameworksBuildPhase
        assert isinstance(results[1], XCSwiftPackageProductDependency)
        assert project.objects.get_objects_in_section('PBXFrameworksBuildPhase')[0].files.__len__() == 1
        assert project.objects.get_objects_in_section('PBXNativeTarget')[0].packageProductDependencies.__len__() == 1
        assert project.objects.get_objects_in_section('PBXBuildFile').__len__() == 1

    def testAddPackageWithTwoProducts(self):
        project = XcodeProject({
            'objects': {
                '0': {'isa': 'PBXNativeTarget', 'name': 'app', 'buildPhases': []},
                'project': {'isa': 'PBXProject'}
            }
        })
        results = project.add_package('http://myrepo.com/some-package', { 
            "kind": "upToNextMajorVersion",
            "minimumVersion": "5.0.1"}, ['some-package','other-package'], 'app')

        # create two package product dependency and their entry into PBXNativeTarget package product depedency, 
        # PBXBuildFile and PBXFrameworksBuildPhase
        assert isinstance(results[1], XCSwiftPackageProductDependency)
        assert isinstance(results[2], XCSwiftPackageProductDependency)
        assert project.objects.get_objects_in_section('PBXFrameworksBuildPhase')[0].files.__len__() == 2
        assert project.objects.get_objects_in_section('PBXNativeTarget')[0].packageProductDependencies.__len__() == 2
        assert project.objects.get_objects_in_section('PBXBuildFile').__len__() == 2

    def testGetPackageReference(self):
        project = XcodeProject({
            'objects': {
                '0': {'isa': 'XCRemoteSwiftPackageReference', 'repositoryURL': 'http://myrepo.com/some-package' }
            }
        })

        result = project.get_or_create_package_reference('http://myrepo.com/some-package', {})
        assert result is not None

    def testGetPackageDependency(self):
        project = XcodeProject({
            'objects': {
                '0': {'isa': 'XCSwiftPackageProductDependency', 'productName': 'Some Product' }
            }
        })

        result = project.get_or_create_package_dependency('Some Product', '', {})
        assert result is not None

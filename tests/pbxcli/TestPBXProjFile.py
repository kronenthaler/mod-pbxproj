import os
import shutil
import sys
import unittest

import pbxproj.pbxcli.pbxproj_file as pbxproj_file
from pbxproj import PBXGenericObject
from pbxproj.pbxcli import open_project, PROJECT_PLACEHOLDER, PATH_PLACEHOLDER
from tests.pbxcli import BASE_PROJECT_PATH, SAMPLE_PROJECT_PATH
import pytest


class PBXProjFileTest(unittest.TestCase):
    def setUp(self):
        # copy the project.pbxproj, into a file that can be used by the tests
        self.pwd = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

        shutil.copyfile(BASE_PROJECT_PATH, SAMPLE_PROJECT_PATH)

    def tearDown(self):
        os.remove(SAMPLE_PROJECT_PATH)
        sys.stdout = sys.__stdout__
        os.chdir(self.pwd)

    def testRemoveFileUnknown(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'whatever',
            '--tree': 'SOURCE_ROOT',
            '--delete': True,
            '--target': None
        }

        project = open_project(args)
        with pytest.raises(Exception, match='^An error occurred removing one of the files.'):
            pbxproj_file.execute(project, args)

    def testRemoveFileKnown(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'AppDelegate.swift',
            '--tree': '<group>',
            '--delete': True,
            '--target': None
        }

        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER], tree=args['--tree']) is not None
        assert project.get_files_by_path(args[PATH_PLACEHOLDER], tree=args['--tree']).__len__() > 0

        result = pbxproj_file.execute(project, args)
        assert result == 'File removed from the project.'

        assert project.get_files_by_path(args[PATH_PLACEHOLDER], tree=args['--tree']) == []

    def testAddFilesNoResult(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'samples/testLibrary.a',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--parent': None,
            '--delete': False,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': True
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]) == []
        result = pbxproj_file.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]).__len__() > 0
        assert result == 'File added to the project, no build file sections created.'

    def testAddFilesError(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: '/samples/testLibrary.a',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--parent': None,
            '--delete': False,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': True
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]) == []
        with pytest.raises(Exception, match='^No files were added to the project.'):
            pbxproj_file.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]).__len__() == 0

    def testAddFilesSuccess(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'samples/testLibrary.a',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--parent': None,
            '--delete': False,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': False
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]) == []
        result = pbxproj_file.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]).__len__() > 0
        assert result == 'File added to the project.\n3 PBXBuildFile sections created.'

    def testAddFilesWithParentNoResult(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'samples/testLibrary.a',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--parent': 'Samples',
            '--delete': False,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': True
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]) == []
        result = pbxproj_file.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]).__len__() > 0
        assert result == 'File added to the project, no build file sections created.'


    def testAddFilesWithParentError(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: '/samples/testLibrary.a',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--parent': 'Samples',
            '--delete': False,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': True
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]) == []
        with pytest.raises(Exception, match='^No files were added to the project.'):
            pbxproj_file.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]).__len__() == 0


    def testAddFilesWithParentSuccess(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'samples/testLibrary.a',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--parent': 'Samples',
            '--delete': False,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': False
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]) == []
        result = pbxproj_file.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]).__len__() > 0
        assert result == 'File added to the project.\n3 PBXBuildFile sections created.'

    def testAddFilesWithHeadersScope(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'samples/dirA/dirB/fileB.h',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--parent': 'Samples',
            '--delete': False,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': False,
            '--header-scope': 'public'
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]) == []
        result = pbxproj_file.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]).__len__() > 0
        assert result == 'File added to the project.\n3 PBXBuildFile sections created.'
        file = project.get_files_by_name('fileB.h')
        build_file = project.get_build_files_for_file(file[0].get_id())
        assert build_file[0].settings.__repr__() == PBXGenericObject().parse({"ATTRIBUTES": ['Public']}).__repr__()

import os
import shutil
import sys
import unittest

import pbxproj.pbxcli.pbxproj_folder as pbxproj_folder
from pbxproj import PBXGenericObject
from pbxproj.pbxcli import open_project, PROJECT_PLACEHOLDER, PATH_PLACEHOLDER
from pbxproj.pbxextensions.ProjectFiles import TreeType
from tests.pbxcli import BASE_PROJECT_PATH, SAMPLE_PROJECT_PATH
import pytest


class PBXProjFolderTest(unittest.TestCase):

    def setUp(self):
        self.pwd = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

        # copy the project.pbxproj, into a file that can be used by the tests
        shutil.copyfile(BASE_PROJECT_PATH, SAMPLE_PROJECT_PATH)

    def tearDown(self):
        os.remove(SAMPLE_PROJECT_PATH)
        sys.stdout = sys.__stdout__
        os.chdir(self.pwd)

    def testRemoveFolderUnknown(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'whatever',
            '--tree': 'SOURCE_ROOT',
            '--delete': True,
            '--target': None
        }

        project = open_project(args)
        with pytest.raises(Exception, match='^An error occurred removing one of the files.'):
            pbxproj_folder.execute(project, args)

    def testRemoveFolderKnown(self):
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

        result = pbxproj_folder.execute(project, args)
        assert result == 'Folder removed from the project.'

        assert project.get_files_by_path(args[PATH_PLACEHOLDER], tree=args['--tree']) == []

    def testAddFolderNoResult(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'samples',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--delete': False,
            '--recursive': False,
            '--exclude': None,
            '--no-create-groups': True,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': True
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER], tree=TreeType.GROUP) == []
        result = pbxproj_folder.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER], tree=TreeType.GROUP).__len__() > 0
        assert result == 'Folder added to the project, no build file sections created.'

    def testAddFolderError(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: '/samples/',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--delete': False,
            '--recursive': False,
            '--exclude': None,
            '--no-create-groups': True,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': True
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER], tree=TreeType.GROUP) == []
        with pytest.raises(Exception, match='^No files were added to the project.'):
            pbxproj_folder.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER], tree=TreeType.GROUP).__len__() == 0

    def testAddFolderSuccess(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'samples',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--delete': False,
            '--recursive': False,
            '--exclude': None,
            '--no-create-groups': False,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': False
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]+'/path with spaces/testLibrary.a',
                                                       tree=TreeType.GROUP) == []
        result = pbxproj_folder.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]+'/path with spaces/testLibrary.a',
                                                   tree=TreeType.GROUP).__len__() == 0
        assert result == 'Folder added to the project.\n6 PBXBuildFile sections created.'

    def testAddFolderSuccessRecursive(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'samples',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--delete': False,
            '--recursive': True,
            '--exclude': None,
            '--no-create-groups': False,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': False
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]+'/path with spaces/testLibrary.a',
                                                       tree=TreeType.GROUP) == []
        result = pbxproj_folder.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]+'/path with spaces/testLibrary.a',
                                                     tree=TreeType.GROUP).__len__() > 0
        assert result == 'Folder added to the project.\n18 PBXBuildFile sections created.'

    def testAddFolderSuccessWithPublicHeaders(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            PATH_PLACEHOLDER: 'samples',
            '--target': None,
            '--tree': 'SOURCE_ROOT',
            '--delete': False,
            '--recursive': True,
            '--exclude': None,
            '--no-create-groups': False,
            '--weak': False,
            '--no-embed': False,
            '--sign-on-copy': False,
            '--ignore-unknown-types': False,
            '--no-create-build-files': False,
            '--header-scope': 'public'
        }
        project = open_project(args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]+'/path with spaces/testLibrary.a',
                                                       tree=TreeType.GROUP) == []
        result = pbxproj_folder.execute(project, args)

        assert project.get_files_by_path(args[PATH_PLACEHOLDER]+'/path with spaces/testLibrary.a',
                                                     tree=TreeType.GROUP).__len__() > 0
        assert result == 'Folder added to the project.\n18 PBXBuildFile sections created.'
        file = project.get_files_by_name('fileB.h')
        build_file = project.get_build_files_for_file(file[0].get_id())
        assert build_file[0].settings.__repr__() == \
                         PBXGenericObject().parse({"ATTRIBUTES": ['Public']}).__repr__()

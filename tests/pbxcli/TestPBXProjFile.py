import unittest
import shutil
import sys
from pbxproj.pbxcli import *
import pbxproj.pbxcli.pbxproj_file as pbxproj_file

class PBXProjFileTest(unittest.TestCase):
    def setUp(self):
        # copy the project.pbxproj, into a file that can be used by the tests
        shutil.copyfile('samplescli/project.pbxproj', 'samplescli/test.pbxproj')

    def tearDown(self):
        os.remove('samplescli/test.pbxproj')
        sys.stdout = sys.__stdout__

    def testRemoveFileUnknown(self):
        args = {
            '<project>': 'samplescli/test.pbxproj',
            '<path>': 'whatever',
            '--tree': 'SOURCE_ROOT',
            '--delete': True,
            '--target': None
        }

        project = open_project(args)
        with self.assertRaisesRegex(Exception, '^An error occurred removing one of the files.'):
            pbxproj_file.execute(project, args)

    def testRemoveFileKnown(self):
        args = {
            '<project>': 'samplescli/test.pbxproj',
            '<path>': 'AppDelegate.swift',
            '--tree': '<group>',
            '--delete': True,
            '--target': None
        }

        project = open_project(args)

        self.assertIsNotNone(project.get_files_by_path(args['<path>'], tree=args['--tree']))
        self.assertGreater(project.get_files_by_path(args['<path>'], tree=args['--tree']).__len__(), 0)

        result = pbxproj_file.execute(project, args)
        self.assertEqual(result, 'File removed from the project.')

        self.assertListEqual(project.get_files_by_path(args['<path>'], tree=args['--tree']), [])

    def testAddFilesNoResult(self):
        args = {
            '<project>': 'samplescli/test.pbxproj',
            '<path>': 'samples/testLibrary.a',
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

        self.assertListEqual(project.get_files_by_path(args['<path>']), [])
        result = pbxproj_file.execute(project, args)

        self.assertGreater(project.get_files_by_path(args['<path>']).__len__(), 0)
        self.assertEqual(result, 'File added to the project, no build file sections created.')

    def testAddFilesError(self):
        args = {
            '<project>': 'samplescli/test.pbxproj',
            '<path>': '/samples/testLibrary.a',
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

        self.assertListEqual(project.get_files_by_path(args['<path>']), [])
        with self.assertRaisesRegex(Exception, '^No files were added to the project.'):
            pbxproj_file.execute(project, args)

        self.assertEqual(project.get_files_by_path(args['<path>']).__len__(), 0)

    def testAddFilesSuccess(self):
        args = {
            '<project>': 'samplescli/test.pbxproj',
            '<path>': 'samples/testLibrary.a',
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

        self.assertListEqual(project.get_files_by_path(args['<path>']), [])
        result = pbxproj_file.execute(project, args)

        self.assertGreater(project.get_files_by_path(args['<path>']).__len__(), 0)
        self.assertEqual(result, 'File added to the project.\n3 PBXBuildFile sections created.')

    def testAddFilesWithParentNoResult(self):
        args = {
            '<project>': 'samplescli/test.pbxproj',
            '<path>': 'samples/testLibrary.a',
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

        self.assertListEqual(project.get_files_by_path(args['<path>']), [])
        result = pbxproj_file.execute(project, args)

        self.assertGreater(project.get_files_by_path(args['<path>']).__len__(), 0)
        self.assertEqual(result, 'File added to the project, no build file sections created.')


    def testAddFilesWithParentError(self):
        args = {
            '<project>': 'samplescli/test.pbxproj',
            '<path>': '/samples/testLibrary.a',
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

        self.assertListEqual(project.get_files_by_path(args['<path>']), [])
        with self.assertRaisesRegex(Exception, '^No files were added to the project.'):
            pbxproj_file.execute(project, args)

        self.assertEqual(project.get_files_by_path(args['<path>']).__len__(), 0)


    def testAddFilesWithParentSuccess(self):
        args = {
            '<project>': 'samplescli/test.pbxproj',
            '<path>': 'samples/testLibrary.a',
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

        self.assertListEqual(project.get_files_by_path(args['<path>']), [])
        result = pbxproj_file.execute(project, args)

        self.assertGreater(project.get_files_by_path(args['<path>']).__len__(), 0)
        self.assertEqual(result, 'File added to the project.\n3 PBXBuildFile sections created.')

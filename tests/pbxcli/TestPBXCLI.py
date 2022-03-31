import os
import sys
import tempfile
import unittest
from io import StringIO

from pbxproj import XcodeProject
from pbxproj.pbxcli import open_project, resolve_backup, backup_project, command_parser, PROJECT_PLACEHOLDER
from tests.pbxcli import BASE_PROJECT_PATH


class PBXCLITest(unittest.TestCase):
    def tearDown(self):
        if hasattr(self, 'backup_file') and self.backup_file:
            os.remove(self.backup_file)
        sys.stdout = sys.__stdout__

    def testOpenProjectWithFullPath(self):
        project = open_project({PROJECT_PLACEHOLDER: BASE_PROJECT_PATH})
        self.assertIsNotNone(project)

    def testOpenProjectWithDirectory(self):
        project = open_project({PROJECT_PLACEHOLDER: 'samplescli'})
        self.assertIsNotNone(project)

    def testLoadingPlistFormat(self):
        project = open_project({PROJECT_PLACEHOLDER: 'samplescli/plist.pbxproj'})
        self.assertIsNotNone(project)

    def testOpenProjectInvalidPath(self):
        with self.assertRaisesRegex(Exception, '^Project file not found'):
            open_project({PROJECT_PLACEHOLDER: 'whatever'})

    def testBackupNoFlag(self):
        project = XcodeProject({}, path=BASE_PROJECT_PATH)
        self.backup_file = backup_project(project, {'--backup': False})
        self.assertIsNone(self.backup_file)

    def testBackupWithFlag(self):
        project = XcodeProject({}, path=BASE_PROJECT_PATH)
        self.backup_file = backup_project(project, {'--backup': True})
        self.assertIsNotNone(self.backup_file)

    def testResolveBackupWithoutFlag(self):
        project = XcodeProject({}, path=BASE_PROJECT_PATH)
        setattr(project, 'save', lambda: True)
        tmpfile = tempfile.NamedTemporaryFile()

        resolve_backup(project, tmpfile.name, {'--backup': False})

        self.assertTrue(os.path.exists(tmpfile.name))

    def testResolveBackupWithFlag(self):
        project = XcodeProject({}, path=BASE_PROJECT_PATH)
        setattr(project, 'save', lambda: True)
        tmpfile = tempfile.NamedTemporaryFile(delete=False)

        resolve_backup(project, tmpfile.name, {'--backup': True})

        self.assertFalse(os.path.exists(tmpfile.name))

    def testCommandWithSuccess(self):
        function = lambda p, a: u'test'
        parser = command_parser(function)
        sys.stdout = StringIO()
        parser({PROJECT_PLACEHOLDER: BASE_PROJECT_PATH, u'--backup': False})
        self.assertEqual(sys.stdout.getvalue().strip(), u'test')

    def testCommandWithFailure(self):
        function = lambda p, a: u'test'
        parser = command_parser(function)
        sys.stdout = StringIO()
        with self.assertRaisesRegex(SystemExit, '^1'):
            parser({PROJECT_PLACEHOLDER: u'whatever/project.pbxproj', u'--backup': False})
        self.assertEqual(sys.stdout.getvalue().strip(), u'Project file not found')

    def testOpenFileWithBrokenReferences(self):
        sys.stderr = StringIO()
        _ = open_project({PROJECT_PLACEHOLDER: 'samplescli/broken-references.pbxproj'})
        self.assertEqual(sys.stderr.getvalue().strip(), '[WARNING] The project contains missing/broken references that '
                                                        'may cause other problems. Open your project in Xcode and '
                                                        'resolve all red-colored files.')

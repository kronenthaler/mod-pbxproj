import os
import sys
import tempfile
import unittest
from io import StringIO

from pbxproj import XcodeProject
from pbxproj.pbxcli import open_project, resolve_backup, backup_project, command_parser, PROJECT_PLACEHOLDER
import pytest

BASE_PROJECT_PATH = 'samplescli/project.pbxproj'


class PBXCLITest(unittest.TestCase):
    def tearDown(self):
        if hasattr(self, 'backup_file') and self.backup_file:
            os.remove(self.backup_file)
        sys.stdout = sys.__stdout__

    def testOpenProjectWithFullPath(self):
        project = open_project({PROJECT_PLACEHOLDER: BASE_PROJECT_PATH})
        assert project is not None

    def testOpenProjectWithDirectory(self):
        project = open_project({PROJECT_PLACEHOLDER: 'samplescli'})
        assert project is not None

    def testLoadingPlistFormat(self):
        project = open_project({PROJECT_PLACEHOLDER: 'samplescli/plist.pbxproj'})
        assert project is not None

    def testOpenProjectInvalidPath(self):
        with pytest.raises(Exception, match='^Project file not found'):
            open_project({PROJECT_PLACEHOLDER: 'whatever'})

    def testBackupNoFlag(self):
        project = XcodeProject({}, path=BASE_PROJECT_PATH)
        self.backup_file = backup_project(project, {'--backup': False})
        assert self.backup_file is None

    def testBackupWithFlag(self):
        project = XcodeProject({}, path=BASE_PROJECT_PATH)
        self.backup_file = backup_project(project, {'--backup': True})
        assert self.backup_file is not None

    def testResolveBackupWithoutFlag(self):
        project = XcodeProject({}, path=BASE_PROJECT_PATH)
        setattr(project, 'save', lambda: True)
        tmpfile = tempfile.NamedTemporaryFile()

        resolve_backup(project, tmpfile.name, {'--backup': False})

        assert os.path.exists(tmpfile.name)

    def testResolveBackupWithFlag(self):
        project = XcodeProject({}, path=BASE_PROJECT_PATH)
        setattr(project, 'save', lambda: True)
        tmpfile = tempfile.NamedTemporaryFile(delete=False)

        resolve_backup(project, tmpfile.name, {'--backup': True})

        assert not os.path.exists(tmpfile.name)

    def testCommandWithSuccess(self):
        function = lambda p, a: u'test'
        parser = command_parser(function)
        sys.stdout = StringIO()
        parser({PROJECT_PLACEHOLDER: BASE_PROJECT_PATH, u'--backup': False})
        assert sys.stdout.getvalue().strip() == u'test'

    def testCommandWithFailure(self):
        function = lambda p, a: u'test'
        parser = command_parser(function)
        sys.stdout = StringIO()
        with pytest.raises(SystemExit, match='^1'):
            parser({PROJECT_PLACEHOLDER: u'whatever/project.pbxproj', u'--backup': False})
        assert sys.stdout.getvalue().strip() == u'Project file not found'

    def testOpenFileWithBrokenReferences(self):
        sys.stderr = StringIO()
        _ = open_project({PROJECT_PLACEHOLDER: 'samplescli/broken-references.pbxproj'})
        assert sys.stderr.getvalue().strip() == '[WARNING] The project contains missing/broken references that ' \
                                                        'may cause other problems. Open your project in Xcode and ' \
                                                        'resolve all red-colored files.'

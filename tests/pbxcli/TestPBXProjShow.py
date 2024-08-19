import os
import shutil
import sys
import unittest

import pbxproj.pbxcli.pbxproj_show as pbxproj_show
from pbxproj.pbxcli import open_project, PROJECT_PLACEHOLDER
from tests.pbxcli import SAMPLE_PROJECT_PATH, BASE_PROJECT_PATH


class PBXProjShowTest(unittest.TestCase):
    def setUp(self):
        self.pwd = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

        # copy the project.pbxproj, into a file that can be used by the tests
        shutil.copyfile(BASE_PROJECT_PATH, SAMPLE_PROJECT_PATH)

    def tearDown(self):
        os.remove(SAMPLE_PROJECT_PATH)
        sys.stdout = sys.__stdout__
        os.chdir(self.pwd)

    def testShowAllTargetsInfo(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            u'--target': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        assert 'testUITests:' in result
        assert 'Product name: testUITests' in result
        assert 'Configurations: Debug, Release' in result
        assert 'Sources (PBXSourcesBuildPhase) file count: 1' in result

        assert 'test:' in result
        assert 'Product name: test\n' in result
        assert 'Configurations: Debug, Release' in result
        assert 'Sources (PBXSourcesBuildPhase) file count: 2' in result

    def testShowTargetBasicInfo(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            u'--target': u'test',
            u'--source-files': None,
            u'--header-files': None,
            u'--resource-files': None,
            u'--framework-files': None,
            u'--configurations': None,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        assert 'testUITests:' not in result
        assert 'Product name: testUITests' not in result

        assert 'test:' in result
        assert 'Product name: test\n' in result

    def testShowTargetConfigurations(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            u'--target': u'test',
            u'--source-files': None,
            u'--header-files': None,
            u'--resource-files': None,
            u'--framework-files': None,
            u'--configurations': True,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        assert 'test:' in result
        assert 'Product name: test\n' in result
        assert 'Configurations: Debug, Release\n' in result

    def testShowTargetSources(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            u'--target': u'test',
            u'--source-files': True,
            u'--header-files': None,
            u'--resource-files': None,
            u'--framework-files': None,
            u'--configurations': None,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        assert 'test:' in result
        assert 'Product name: test\n' in result
        assert 'Sources:' in result
        assert 'AppDelegate.swift' in result
        assert 'VīęwČøntröłler.swift' in result

    def testShowTargetResources(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            u'--target': u'test',
            u'--source-files': None,
            u'--header-files': None,
            u'--resource-files': True,
            u'--framework-files': None,
            u'--configurations': None,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        assert 'test:' in result
        assert 'Product name: test\n' in result
        assert 'Resources:' in result
        assert 'Assets.xcassets' in result
        assert 'LaunchScreen.storyboard' in result
        assert 'Main.storyboard' in result

    def testShowTargetHeaders(self):
        args = {
            PROJECT_PLACEHOLDER: u'samplescli/dependency.xcodeproj/project.pbxproj',
            u'--target': u'helloworld',
            u'--source-files': None,
            u'--header-files': True,
            u'--resource-files': None,
            u'--framework-files': None,
            u'--configurations': None,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        assert 'helloworld:' in result
        assert 'Product name: helloworld\n' in result
        assert 'Headers:' in result
        assert 'doit.h' in result
        assert 'helloworld.h' in result

    def testShowTargetFrameworks(self):
        args = {
            PROJECT_PLACEHOLDER: u'samplescli/dependency.xcodeproj/project.pbxproj',
            u'--target': u'helloworld',
            u'--source-files': None,
            u'--header-files': None,
            u'--resource-files': None,
            u'--framework-files': True,
            u'--configurations': None,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        assert 'helloworld:' in result
        assert 'Product name: helloworld\n' in result
        assert 'Frameworks:' in result
        assert 'AppKit.framework' in result

    def testShowTargetExplicitBuildPhase(self):
        args = {
            PROJECT_PLACEHOLDER: u'samplescli/dependency.xcodeproj/project.pbxproj',
            u'--target': u'helloworld',
            u'--source-files': None,
            u'--header-files': None,
            u'--resource-files': None,
            u'--framework-files': None,
            u'--configurations': None,
            u'--build-phase-files': u'PBXFrameworksBuildPhase'
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        assert 'helloworld:' in result
        assert 'Product name: helloworld\n' in result
        assert 'Frameworks:' in result
        assert 'AppKit.framework' in result

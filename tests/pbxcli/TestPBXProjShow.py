import os
import shutil
import sys
import unittest

import pbxproj.pbxcli.pbxproj_show as pbxproj_show
from pbxproj.pbxcli import open_project, PROJECT_PLACEHOLDER
from tests.pbxcli import SAMPLE_PROJECT_PATH, BASE_PROJECT_PATH


class PBXProjShowTest(unittest.TestCase):
    def setUp(self):
        # copy the project.pbxproj, into a file that can be used by the tests
        shutil.copyfile(BASE_PROJECT_PATH, SAMPLE_PROJECT_PATH)

    def tearDown(self):
        os.remove(SAMPLE_PROJECT_PATH)
        sys.stdout = sys.__stdout__

    def testShowAllTargetsInfo(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            u'--target': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        self.assertIn('testUITests:', result)
        self.assertIn('Product name: testUITests', result)
        self.assertIn('Configurations: Debug, Release', result)
        self.assertIn('Sources (PBXSourcesBuildPhase) file count: 1', result)

        self.assertIn('test:', result)
        self.assertIn('Product name: test\n', result)
        self.assertIn('Configurations: Debug, Release', result)
        self.assertIn('Sources (PBXSourcesBuildPhase) file count: 2', result)

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

        self.assertNotIn('testUITests:', result)
        self.assertNotIn('Product name: testUITests', result)

        self.assertIn('test:', result)
        self.assertIn('Product name: test\n', result)

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

        self.assertIn('test:', result)
        self.assertIn('Product name: test\n', result)
        self.assertIn('Configurations: Debug, Release\n', result)

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

        self.assertIn('test:', result)
        self.assertIn('Product name: test\n', result)
        self.assertIn('Sources:', result)
        self.assertIn('AppDelegate.swift', result)
        self.assertIn('VīęwČøntröłler.swift', result)

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

        self.assertIn('test:', result)
        self.assertIn('Product name: test\n', result)
        self.assertIn('Resources:', result)
        self.assertIn('Assets.xcassets', result)
        self.assertIn('LaunchScreen.storyboard', result)
        self.assertIn('Main.storyboard', result)

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

        self.assertIn('helloworld:', result)
        self.assertIn('Product name: helloworld\n', result)
        self.assertIn('Headers:', result)
        self.assertIn('doit.h', result)
        self.assertIn('helloworld.h', result)

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

        self.assertIn('helloworld:', result)
        self.assertIn('Product name: helloworld\n', result)
        self.assertIn('Frameworks:', result)
        self.assertIn('AppKit.framework', result)

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

        self.assertIn('helloworld:', result)
        self.assertIn('Product name: helloworld\n', result)
        self.assertIn('Frameworks:', result)
        self.assertIn('AppKit.framework', result)
